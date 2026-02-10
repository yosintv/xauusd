/**
 * CONFIGURATION SECTION
 * Add your stream IDs and URLs here
 */
const streamConfig = {
    "1": "https://pull.niur.live/live/stream-406865_lsd.m3u8?txSecret=8ad7f2587aa2b77cdc69528aa197c449&txTime=698b488a",
    "2": "https://example.com/stream2.m3u8",
    "3": "https://example.com/stream3.mpd",
    "test": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
};

// Function to get the ID from the URL (e.g., ?id=1)
function getStreamId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function loadPlayer() {
    const id = getStreamId();
    const streamUrl = streamConfig[id];

    // If no ID is provided or ID doesn't exist in config
    if (!id || !streamUrl) {
        document.getElementById('jwplayerDiv').innerHTML = `
            <div class="error-msg">
                <h2>Invalid Stream ID</h2>
                <p>Please use <strong>?id=1</strong> or another valid ID in the URL.</p>
            </div>`;
        return;
    }

    // Detect if it's DASH (.mpd) or HLS (.m3u8)
    const type = streamUrl.includes('.mpd') ? 'dash' : 'hls';

    // Setup JWPlayer
    jwplayer("jwplayerDiv").setup({
        file: streamUrl,
        type: type,
        autostart: true,
        stretching: "uniform",
        width: "100%",
        height: "100%",
        cast: {} // Enables Chromecast if supported
    });
}

// Wait for JWPlayer library to be ready
function checkLib() {
    if (typeof jwplayer === 'function') {
        loadPlayer();
    } else {
        setTimeout(checkLib, 100);
    }
}

// Execute when window loads
window.onload = checkLib;
