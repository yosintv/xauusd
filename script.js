/**
 * CONFIGURATION SECTION
 * For standard streams: use the URL string.
 * For DRM streams: use { url, kid, key }.
 * For iframe sources: use { url, type: "iframe" }.
 */
const streamConfig = {
    // 1. Standard HLS Stream
    "1": "https://pull.niur.live/live/stream-406865_lsd.m3u8?txSecret=8ad7f2587aa2b77cdc69528aa197c449&txTime=698b488a",
    "willow": "https://ortdruuckehagkdtgwevu.poocloud.in/secure/NpjgELwuGLGoipabmSzEhFYQAbPtwlWV/0/1770802533/streamed-willow/index.m3u8",



    // 2. Iframe Player Option
    "player4": {
        "type": "iframe",
        "url": "https://embedsports.top/embed/admin/admin-willow-cricket/2"
    },

    // 3. DASH Stream with ClearKey DRM
    "primecricket": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/dash/enc/pajvg2ord7/out/v1/564bb083afea4561a5a60c4447258379/cenc.mpd",
        "kid": "75902b6304efb1d6323c833d42347d68", 
        "key": "70c40016a0bba8ddc3aabcee112970c8"
    },
    
    
    // 4. Standard DASH Stream (No DRM)
    "3": "https://dash.akamaized.net/envivio/EnvivioDash3/manifest.mpd"
};

function getStreamId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function loadPlayer() {
    const id = getStreamId();
    const config = streamConfig[id];
    const playerDiv = document.getElementById('jwplayerDiv');

    if (!id || !config) {
        playerDiv.innerHTML = `
            <div class="error-msg">
                <h2>Invalid or Missing Stream ID</h2>
                <p>Use ?id=1 or ?id=primecricket in the URL</p>
            </div>`;
        return;
    }

    const isObject = typeof config === 'object';
    const streamUrl = isObject ? config.url : config;
    const isIframe = isObject && config.type === "iframe";

    // IFRAME LOGIC: If type is iframe, inject the iframe and stop
    if (isIframe) {
        playerDiv.innerHTML = `<iframe src="${streamUrl}" frameborder="0" scrolling="no" allowfullscreen="true" style="width:100%; height:100%; position:absolute; top:0; left:0;"></iframe>`;
        return;
    }

    // VIDEO PLAYER LOGIC: Handle M3U8 and MPD
    const kid = isObject ? config.kid : null;
    const key = isObject ? config.key : null;
    const streamType = streamUrl.toLowerCase().includes(".mpd") ? "dash" : "hls";

    let playerSetup = {
        file: streamUrl,
        image: "https://web.cricfoot.net/logo.png",
        type: streamType,
        autostart: true,
        mute: false,
        volume: 100,
        stretching: "uniform",
        width: "100%",
        height: "100%",
        cast: {}
    };

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
