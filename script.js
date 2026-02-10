/**
 * CONFIGURATION SECTION
 */
const streamConfig = {
    "1": "https://pull.niur.live/live/stream-406865_lsd.m3u8?txSecret=8ad7f2587aa2b77cdc69528aa197c449&txTime=698b488a",
    "primecricket": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/dash/enc/pajvg2ord7/out/v1/564bb083afea4561a5a60c4447258379/cenc.mpd",
        "kid": "75902b6304efb1d6323c833d42347d68", 
        "key": "70c40016a0bba8ddc3aabcee112970c8"
    },
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
                <h2>Invalid Stream ID</h2>
                <p>Use ?id=1 or ?id=primecricket</p>
            </div>`;
        return;
    }

    const isObject = typeof config === 'object';
    const streamUrl = isObject ? config.url : config;
    const kid = isObject ? config.kid : null;
    const key = isObject ? config.key : null;
    const streamType = streamUrl.toLowerCase().includes(".mpd") ? "dash" : "hls";

    const playerInstance = jwplayer("jwplayerDiv");

    playerInstance.setup({
        file: streamUrl,
        image: "https://web.cricfoot.net/logo.png",
        type: streamType,
        autostart: false, // Changed to false to allow user to trigger sound
        mute: false,
        volume: 100,
        stretching: "uniform",
        width: "100%",
        height: "100%",
        drm: (kid && key) ? { clearkey: { keyId: kid, key: key } } : {}
    });

    // FORCE UNMUTE ON PLAY
    playerInstance.on('play', function() {
        playerInstance.setMute(false);
        playerInstance.setVolume(100);
    });

    // Auto-attempt play (if browser allows it will start, if not it waits for click)
    playerInstance.play();
}

function checkLib() {
    if (typeof jwplayer === 'function') {
        loadPlayer();
    } else {
        setTimeout(checkLib, 100);
    }
}

window.onload = checkLib;
