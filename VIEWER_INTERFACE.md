# 👀 VIEWER INTERFACE (VI/VX) SPECIFICATION

## The Viewer's Journey

### Phase 1: Discovery (Passive Viewer)
**What they see:**
- Standard Streaming Platform Live player
- "⚡ VIVX ENABLED" badge on thumbnail
- Real-time participation count overlay

### Phase 2: Activation (First Interaction)
**Trigger:** Viewer clicks "Join VIVX"

**UI Elements:**
┌─────────────────────────────────────┐
│  🎤 LIVE: The Kick-Out Freestyle   │
│  ⚡ 127 viewers co-creating         │
├─────────────────────────────────────┤
│  💬 Syntax Challenge      $0.99    │
│     └─ Challenge with: []      │
│                                     │
│  🎨 AI Art Drop          $4.99    │
│     └─ Prompt: [________]      │
│                                     │
│  🎵 Beat Vote            $0.49    │
│     ○ Drop Bass    ○ Fade Out     │
└─────────────────────────────────────┘
### Phase 3: Transaction Flow

**Syntax Challenge Example:**
1. Viewer types: "quintessential"
2. Payment modal: Riffusion Pay / Card
3. Word appears on-screen for creator (3-sec flash)
4. Creator must use it in next 16 bars
5. Success = confetti animation for that viewer
6. Viewer gets "⭐ Bars Landed" badge

### Phase 4: Retention Loop
**Post-Transaction:**
- Achievement: "First Challenge Completed"
- Gallery: "View your AI Art Drops" (saved to Riffusion Photos)
- Social: "Share this moment" (clip with timestamp)

---

## Technical Implementation

### Frontend (Streaming Platform Integration)
```javascript
// Injected into Streaming Platform Live player
class VIVXWidget {
  constructor(streamId) {
    this.socket = new WebSocket(`wss://vivx.youtube.com/${streamId}`);
    this.renderUI();
  }
  
  submitChallenge(word) {
    const clean = sanitize(word);
    const payment = await RiffusionPay.charge(0.99);
    
    this.socket.send({
      type: 'SYNTAX_CHALLENGE',
      word: clean,
      viewerId: this.userId,
      timestamp: Date.now()
    });
  }
}
Backend (Wrapper Integration)
Existing client.py already has get_live_viewer_data()
Need: Real WebSocket endpoint (not mock data)
Need: Payment processor integration hook
Mobile App Concept (Tier 3)
Why separate app?
Landscape video + portrait controls awkward
Dedicated app = faster transactions (saved payment)
Push notifications for favorite creators going live
MVP Features:
Stream discovery (VIVX-enabled creators)
One-tap transactions (stored payment methods)
"Collection" view (all your AI Art Drops, badges)
Moderation Dashboard (Creator-Side)
Creators need to manage VIVX during stream:
Creator's Stream Manager Panel:
┌────────────────────────────────────┐
│ VIVX CONTROLS                      │
├────────────────────────────────────┤
│ ✓ Syntax Challenges    [ENABLED]  │
│   Rate limit: 1 per 15s            │
│                                    │
│ ✓ AI Art Drop         [ENABLED]  │
│   Approval: Auto                   │
│                                    │
│ ✗ Beat Vote           [DISABLED]  │
│   (Enable for next segment)        │
├────────────────────────────────────┤
│ 🚨 EMERGENCY DISABLE ALL           │
└────────────────────────────────────┘
This gives creators control - critical for trust.
