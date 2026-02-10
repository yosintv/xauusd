/**
 * CONFIGURATION SECTION
 * Standard M3U8/MPD or Iframe links can all be single lines.
 */
const streamConfig = {
    // 1. Direct Stream Links
    "1": "https://pull.niur.live/live/stream-406865_lsd.m3u8?txSecret=8ad7f2587aa2b77cdc69528aa197c449&txTime=698b488a",
    "willow": "https://ortdruuckehagkdtgwevu.poocloud.in/secure/NpjgELwuGLGoipabmSzEhFYQAbPtwlWV/0/1770802533/streamed-willow/index.m3u8",

    
    // 2. New Iframe Link (Loads automatically as iframe)
    "willow1": "https://embedsports.top/embed/admin/admin-willow-cricket/1",
    "willow2": "https://embedsports.top/embed/admin/admin-willow-cricket/2",

    

    // 3. DASH Stream with ClearKey DRM (Still needs object for keys)
    "primecricket": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/dash/enc/pajvg2ord7/out/v1/564bb083afea4561a5a60c4447258379/cenc.mpd",
        "kid": "75902b6304efb1d6323c833d42347d68", 
        "key": "70c40016a0bba8ddc3aabcee112970c8"
    }
};

function getStreamId() {
    return new URLSearchParams(window.location.search).get('id');
}

function loadPlayer() {
    const id = getStreamId();
    const config = streamConfig[id];
    const playerDiv = document.getElementById('jwplayerDiv');

    if (!id || !config) {
        playerDiv.innerHTML = `<div class="error-msg"><h2>Invalid ID</h2><p>Please check your URL parameter.</p></div>`;
        return;
    }

    const isObject = typeof config === 'object';
    const streamUrl = isObject ? config.url : config;

    /**
     * SMART DETECTION:
     * If the URL doesn't end with .m3u8 or .mpd, it loads as an iframe.
     */
    const isVideoFile = streamUrl.toLowerCase().includes('.m3u8') || streamUrl.toLowerCase().includes('.mpd');

    if (!isVideoFile) {
        playerDiv.innerHTML = `<iframe src="${streamUrl}" frameborder="0" scrolling="no" allowfullscreen="true" style="width:100%; height:100%; position:absolute; top:0; left:0; background:#000;"></iframe>`;
        return;
    }

    // JWPLAYER LOGIC (for M3U8/MPD)
    const kid = isObject ? config.kid : null;
    const key = isObject ? config.key : null;
    const streamType = streamUrl.toLowerCase().includes(".mpd") ? "dash" : "hls";

    jwplayer("jwplayerDiv").setup({
        file: streamUrl,
        image: "https://web.cricfoot.net/logo.png",
        type: streamType,
        autostart: true,
        mute: false,
        volume: 100,
        stretching: "uniform",
        width: "100%",
        height: "100%",
        drm: (kid && key) ? { clearkey: { keyId: kid, key: key } } : {},
        cast: {}
    });
}

function checkLib() {
    if (typeof jwplayer === 'function') {
        loadPlayer();
    } else {
        setTimeout(checkLib, 100);
    }
}

window.onload = checkLib;
