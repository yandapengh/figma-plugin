const express = require('express');
const { WebSocketServer } = require('ws');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

let figmaSocket = null;
const pendingRequests = new Map();

const wss = new WebSocketServer({ port: 8767 });

function clearPendingBySocketClose() {
    pendingRequests.forEach((req, id) => {
        clearTimeout(req.timer);
        req.res.status(503).json({
            error: {
                code: 'offline',
                message: 'Figma disconnected while waiting response',
                requestId: id,
                requestType: req.requestType
            }
        });
    });
    pendingRequests.clear();
}

function addPendingRequest(id, requestType, res, timeoutMs) {
    const timer = setTimeout(() => {
        if (!pendingRequests.has(id)) return;
        pendingRequests.delete(id);
        res.status(504).json({
            error: {
                code: 'timeout',
                message: `Request timeout after ${timeoutMs}ms`,
                requestId: id,
                requestType: requestType
            }
        });
    }, timeoutMs);

    pendingRequests.set(id, { res, requestType, timer });
}

wss.on('connection', (ws) => {
    console.log('[Bridge] New connection');
    figmaSocket = ws;

    ws.on('message', (data) => {
        const raw = data.toString();
        if (raw === 'ping') {
            ws.send('pong');
            return;
        }

        try {
            const msg = JSON.parse(raw);

            if (msg.type === 'register' && (msg.client === 'figma' || msg.client === 'ui')) {
                ws.send(JSON.stringify({ type: 'connected' }));
                return;
            }

            if (msg.type === 'response') {
                const pending = pendingRequests.get(msg.id);
                if (!pending) {
                    console.warn('[Bridge] Unmatched response id:', msg.id);
                    return;
                }

                clearTimeout(pending.timer);
                pendingRequests.delete(msg.id);
                pending.res.json({
                    requestId: msg.id,
                    requestType: pending.requestType,
                    result: msg.result
                });
            }
        } catch (e) {
            console.log('[Bridge] Parse error:', e.message);
        }
    });

    ws.on('close', () => {
        console.log('[Bridge] Disconnected');
        figmaSocket = null;
        clearPendingBySocketClose();
    });
});

app.post('/send', (req, res) => {
    if (!figmaSocket || figmaSocket.readyState !== 1) {
        return res.status(503).json({
            error: {
                code: 'offline',
                message: 'Figma offline'
            }
        });
    }

    const id = Date.now() + Math.floor(Math.random() * 1000);
    let code = req.body.code || req.body;
    if (typeof code === 'object') code = code.code;

    figmaSocket.send(JSON.stringify({ type: 'execute', id, code }));
    addPendingRequest(id, 'execute', res, 30000);
});

app.post('/read', (req, res) => {
    if (!figmaSocket || figmaSocket.readyState !== 1) {
        return res.status(503).json({
            error: {
                code: 'offline',
                message: 'Figma offline'
            }
        });
    }

    const id = Date.now() + Math.floor(Math.random() * 1000);
    figmaSocket.send(JSON.stringify({ type: 'read', id }));
    addPendingRequest(id, 'read', res, 10000);
});

app.get('/status', (req, res) => {
    res.json({
        connected: !!(figmaSocket && figmaSocket.readyState === 1),
        pendingRequests: pendingRequests.size
    });
});

app.listen(8768, () => {
    console.log('===========================================');
    console.log('  Bridge: http://localhost:8768');
    console.log('  WS: ws://localhost:8767');
    console.log('===========================================');
});
