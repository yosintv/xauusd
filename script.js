/**
 * CONFIGURATION SECTION
 * For standard streams: just use the URL string.
 * For DRM streams: use the { url, kid, key } object format.
 */
const streamConfig = {
    // 1. Standard HLS Stream
    "1": "https://pull.niur.live/live/stream-406865_lsd.m3u8?txSecret=8ad7f2587aa2b77cdc69528aa197c449&txTime=698b488a",

    // 2. DASH Stream with ClearKey DRM
    "primecricket": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/dash/enc/pajvg2ord7/out/v1/564bb083afea4561a5a60c4447258379/cenc.mpd",
        "kid": "75902b6304efb1d6323c833d42347d68", 
        "key": "70c40016a0bba8ddc3aabcee112970c8"
    },

    // 3. Standard DASH Stream (No DRM)
    "3": "https://dash.akamaized.net/envivio/EnvivioDash3/manifest.mpd"
};

function getStreamId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function loadPlayer() {
    const id = getStreamId();
    const config = streamConfig[id];

    if (!id || !config) {
        document.getElementById('jwplayerDiv').innerHTML = `
            <div class="error-msg">
                <h2>Invalid or Missing Stream ID</h2>
                <p>Use ?id=1 or ?id=2 in the URL</p>
            </div>`;
        return;
    }

    // Extract URL and Keys whether config is a string or an object
    const isObject = typeof config === 'object';
    const streamUrl = isObject ? config.url : config;
    const kid = isObject ? config.kid : null;
    const key = isObject ? config.key : null;

    // Detect Type
    const streamType = streamUrl.toLowerCase().includes(".mpd") ? "dash" : "hls";

    // Build Player Config
    let playerSetup = {
        file: streamUrl,
        type: streamType,
        autostart: true,
        stretching: "uniform",
        width: "100%",
        height: "100%"
    };

    // Add DRM if Keys are present
    if (kid && key) {
        playerSetup.drm = {
            clearkey: {
                keyId: kid,
                key: key
            }
        };
    }

    jwplayer("jwplayerDiv").setup(playerSetup);
}

function checkLib() {
    if (typeof jwplayer === 'function') {
        loadPlayer();
    } else {
        setTimeout(checkLib, 100);
    }
}

window.onload = checkLib;
