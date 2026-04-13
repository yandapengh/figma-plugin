const express = require('express');
const { WebSocketServer } = require('ws');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

let figmaSocket = null;
let pendingRequest = null;

const wss = new WebSocketServer({ port: 8767 });

wss.on('connection', (ws) => {
    console.log('[Bridge] New connection');
    figmaSocket = ws;
    console.log('[Bridge] Registered');
    
    ws.on('message', (data) => {
        var raw = data.toString();
        console.log('[Bridge] WS:', raw.substring(0, 50));
        
        if (raw === 'ping') {
            ws.send('pong');
            return;
        }
        
        try {
            var msg = JSON.parse(raw);
            
            if (msg.type === 'register' && (msg.client === 'figma' || msg.client === 'ui')) {
                ws.send(JSON.stringify({ type: 'connected' }));
                return;
            }
            
            if (msg.type === 'response' && pendingRequest) {
                console.log('[Bridge] Response:', msg.result ? msg.result.substring(0, 30) : 'empty');
                pendingRequest.res.json({ result: msg.result });
                pendingRequest = null;
            }
        } catch (e) {
            console.log('[Bridge] Parse error:', e);
        }
    });
    
    ws.on('close', () => {
        console.log('[Bridge] Disconnected');
        figmaSocket = null;
    });
});

app.post('/send', (req, res) => {
    console.log('[Bridge] /send called');
    
    if (!figmaSocket || figmaSocket.readyState !== 1) {
        console.log('[Bridge] No Figma');
        return res.status(500).json({ error: 'Figma offline' });
    }
    
    var id = Date.now();
    var code = req.body.code || req.body;
    if (typeof code === 'object') code = code.code;
    
    console.log('[Bridge] Code:', code ? code.substring(0, 30) : 'EMPTY');
    figmaSocket.send(JSON.stringify({ type: 'execute', id: id, code: code }));
    
    pendingRequest = { res: res, id: id };
    
    setTimeout(function() {
        if (pendingRequest && pendingRequest.id === id) {
            console.log('[Bridge] Timeout');
            pendingRequest.res.json({ error: 'Timeout' });
            pendingRequest = null;
        }
    }, 30000);
});

app.post('/read', (req, res) => {
    console.log('[Bridge] /read called');
    
    if (!figmaSocket || figmaSocket.readyState !== 1) {
        return res.status(500).json({ error: 'Figma offline' });
    }
    
    var id = Date.now();
    figmaSocket.send(JSON.stringify({ type: 'read', id: id }));
    
    pendingRequest = { res: res, id: id };
    
    setTimeout(function() {
        if (pendingRequest && pendingRequest.id === id) {
            pendingRequest.res.json({ error: 'No selection' });
            pendingRequest = null;
        }
    }, 10000);
});

app.get('/status', (req, res) => {
    res.json({ connected: figmaSocket && figmaSocket.readyState === 1 });
});

app.listen(8768, () => {
    console.log('===========================================');
    console.log('  Bridge: http://localhost:8768');
    console.log('  WS: ws://localhost:8767');
    console.log('===========================================');
});