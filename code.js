figma.showUI(__html__, { visible: true, width: 400, height: 320 });

figma.ui.onmessage = function(msg) {
    console.log('[code.js] Received:', JSON.stringify(msg));
    console.log('[code.js] msg.type:', msg ? msg.type : 'undefined');

    if (msg.type === 'execute') {
        console.log('[code.js] Execute, code:', msg.code ? msg.code.substring(0, 50) : 'NO CODE');
        try {
            if (!msg.code) {
                figma.ui.postMessage({ type: 'result', error: 'Empty code' });
                return;
            }

            var code = msg.code.trim();
            var Fn = Function;
            var wrapped = new Fn('figma', 'return ' + code);
            var result = wrapped(figma);

            if (result && typeof result.then === 'function') {
                result.then(function(r) {
                    figma.ui.postMessage({ type: 'result', data: JSON.stringify(r) });
                }).catch(function(err) {
                    figma.ui.postMessage({ type: 'result', error: err.message });
                });
            } else {
                figma.ui.postMessage({ type: 'result', data: JSON.stringify(result) });
            }
        } catch (err) {
            figma.ui.postMessage({ type: 'result', error: err.message });
        }
    }

    if (msg.type === 'readSelection') {
        readSelection(msg.requestId);
    }
};

function readSelection(requestId) {
    try {
        var selection = figma.currentPage.selection;

        if (selection.length === 0) {
            figma.ui.postMessage({ type: 'readResult', error: '请先选中节点', requestId: requestId });
            return;
        }

        var result = {
            schemaVersion: 'memory-node@1.0.0',
            extractedAt: new Date().toISOString(),
            nodes: []
        };

        for (var i = 0; i < selection.length; i++) {
            result.nodes.push(collectNode(selection[i]));
        }

        figma.ui.postMessage({ type: 'readResult', data: result, requestId: requestId });
    } catch (e) {
        figma.ui.postMessage({ type: 'readResult', error: '读取失败: ' + e.message, requestId: requestId });
    }
}

function collectNode(node) {
    var nodeData = {
        id: node.id,
        type: node.type,
        name: node.name,
        size: {
            width: Math.round(node.width),
            height: Math.round(node.height)
        },
        hierarchy: {
            childCount: node.children ? node.children.length : 0
        },
        autoLayout: extractAutoLayout(node),
        componentSemantics: extractComponentSemantics(node),
        tokens: extractTokens(node)
    };

    if (node.type === 'TEXT') {
        nodeData.text = {
            characters: node.characters || '',
            fontSize: node.fontSize || null,
            fontName: node.fontName || null
        };
    }

    if (node.children && node.children.length > 0) {
        nodeData.children = [];
        for (var i = 0; i < node.children.length; i++) {
            nodeData.children.push(collectNode(node.children[i]));
        }
    }

    return nodeData;
}

function extractAutoLayout(node) {
    var hasLayout = typeof node.layoutMode !== 'undefined' && node.layoutMode !== 'NONE';
    if (!hasLayout) {
        return {
            enabled: false
        };
    }

    return {
        enabled: true,
        direction: node.layoutMode,
        alignment9: mapAlignment9(node),
        spacing: typeof node.itemSpacing === 'number' ? node.itemSpacing : 0,
        padding: {
            top: typeof node.paddingTop === 'number' ? node.paddingTop : 0,
            right: typeof node.paddingRight === 'number' ? node.paddingRight : 0,
            bottom: typeof node.paddingBottom === 'number' ? node.paddingBottom : 0,
            left: typeof node.paddingLeft === 'number' ? node.paddingLeft : 0
        }
    };
}

function mapAlignment9(node) {
    var primary = node.primaryAxisAlignItems || 'MIN';
    var counter = node.counterAxisAlignItems || 'MIN';

    var row = counter === 'MIN' ? 'TOP' : (counter === 'CENTER' ? 'CENTER' : 'BOTTOM');
    var col = primary === 'MIN' ? 'LEFT' : (primary === 'CENTER' ? 'CENTER' : 'RIGHT');

    if (node.layoutMode === 'VERTICAL') {
        row = primary === 'MIN' ? 'TOP' : (primary === 'CENTER' ? 'CENTER' : 'BOTTOM');
        col = counter === 'MIN' ? 'LEFT' : (counter === 'CENTER' ? 'CENTER' : 'RIGHT');
    }

    return row + '_' + col;
}

function extractComponentSemantics(node) {
    return {
        component: !!node.mainComponent,
        variant: !!(node.variantProperties && Object.keys(node.variantProperties).length > 0),
        instance: node.type === 'INSTANCE',
        reference: node.mainComponent ? node.mainComponent.id : null,
        variantProperties: node.variantProperties || null
    };
}

function extractTokens(node) {
    var tokenData = {
        color: [],
        typography: [],
        effect: []
    };

    if (node.boundVariables) {
        if (node.boundVariables.fills) tokenData.color.push(String(node.boundVariables.fills));
        if (node.boundVariables.strokes) tokenData.color.push(String(node.boundVariables.strokes));
        if (node.boundVariables.characters) tokenData.typography.push(String(node.boundVariables.characters));
        if (node.boundVariables.effects) tokenData.effect.push(String(node.boundVariables.effects));
    }

    if (tokenData.color.length === 0 && node.fills && node.fills.length > 0 && node.fills[0].type === 'SOLID') {
        var c = node.fills[0].color;
        tokenData.color.push('#' +
            Math.round(c.r * 255).toString(16).padStart(2, '0') +
            Math.round(c.g * 255).toString(16).padStart(2, '0') +
            Math.round(c.b * 255).toString(16).padStart(2, '0'));
    }

    if (tokenData.effect.length === 0 && node.effects && node.effects.length > 0) {
        tokenData.effect.push('literal:effect:' + node.effects[0].type);
    }

    if (tokenData.typography.length === 0 && node.type === 'TEXT') {
        tokenData.typography.push('literal:fontSize:' + String(node.fontSize || 'unknown'));
    }

    return tokenData;
}
