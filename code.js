figma.showUI(__html__, { visible: true, width: 400, height: 320 });

figma.ui.onmessage = function(msg) {
    console.log('[code.js] Received:', JSON.stringify(msg));
    console.log('[code.js] msg.type:', msg ? msg.type : 'undefined');
    
    if (msg.type === 'execute') {
        console.log('[code.js] Execute, code:', msg.code ? msg.code.substring(0, 50) : 'NO CODE');
        try {
            if (!msg.code) {
                console.log('[code.js] ERROR: msg.code is empty');
                figma.ui.postMessage({ type: 'result', error: 'Empty code' });
                return;
            }
            var code = msg.code.trim();
            console.log('[code.js] Trimmed code:', code.substring(0, 30));
            
            try {
                // 使用同步 Function 而不是 AsyncFunction
                var Fn = Function;
                console.log('[code.js] Step 1: Fn OK');
                var wrapped = new Fn('figma', 'return ' + code);
                console.log('[code.js] Step 2: wrapped OK');
                var result = wrapped(figma);
                console.log('[code.js] Step 3: result OK, type:', typeof result);
            } catch(e) {
                console.log('[code.js] AsyncFn error:', e.message);
                console.log('[code.js] Stack:', e.stack);
                figma.ui.postMessage({ type: 'result', error: e.message });
            }
            
            console.log('[code.js] Result type:', typeof result);
            console.log('[code.js] Is Promise?:', result && typeof result.then === 'function');
            
            if (result && typeof result.then === 'function') {
                result.then(function(r) {
                    console.log('[code.js] Promise resolved:', r);
                    figma.ui.postMessage({ type: 'result', data: JSON.stringify(r) });
                }).catch(function(err) {
                    console.log('[code.js] Promise error:', err.message);
                    figma.ui.postMessage({ type: 'result', error: err.message });
                });
            } else {
                console.log('[code.js] Direct result:', result);
                figma.ui.postMessage({ type: 'result', data: JSON.stringify(result) });
            }
            
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
        
        var result = { nodes: [] };
        
        for (var i = 0; i < selection.length; i++) {
            var node = selection[i];
            var nodeData = collectNode(node);
            result.nodes.push(nodeData);
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
        x: Math.round(node.x),
        y: Math.round(node.y),
        width: Math.round(node.width),
        height: Math.round(node.height)
    };
    
    if (node.fills && node.fills.length > 0 && node.fills[0].type === 'SOLID') {
        var c = node.fills[0].color;
        nodeData.fill = '#' + 
            Math.round(c.r * 255).toString(16).padStart(2, '0') +
            Math.round(c.g * 255).toString(16).padStart(2, '0') +
            Math.round(c.b * 255).toString(16).padStart(2, '0');
    }
    
    if (node.type === 'TEXT') {
        nodeData.text = node.characters || '';
    }
    
    if (node.children && node.children.length > 0) {
        nodeData.children = [];
        for (var i = 0; i < node.children.length; i++) {
            nodeData.children.push(collectNode(node.children[i]));
        }
    }
    
    return nodeData;
}
