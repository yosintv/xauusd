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

    

// New DASH DRM Streams
    "hubsports": {
        "url": "https://mh-bks400-08.starhubgo.com/bpk-token/1ac@pc4zxdfmyh5oubeut3bg32tphstqp43ipaheuwaa/bpk-tv/HubSports4HDnew/output/manifest.mpd",
        "kid": "9a29d4f3b6e540b3aa2f36927c01b6f4",
        "key": "57b670b45b5cb453a9f48fa975b702c1"
    },
    "willow": {
        "url": "https://otte.live.cf.ww.aiv-cdn.net/sin-nitro/live/clients/dash/enc/1ohdhd8cgj/out/v1/99b88a548afa47e5bfc38781e8479c3a/cenc.mpd",
        "kid": "2a4feb551e1b3332f5aaf31ac1bcb8c9",
        "key": "279735c6cba7f9736d0d51eea412f978"
    },
    "primecricket": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/dash/enc/pajvg2ord7/out/v1/564bb083afea4561a5a60c4447258379/cenc.mpd",
        "kid": "75902b6304efb1d6323c833d42347d68",
        "key": "70c40016a0bba8ddc3aabcee112970c8"
    },
    "willowmpd": {
        "url": "https://a201aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/clients/dash/enc/f60kqesunw/out/v1/a435ed7a00f947deb4369b46d8f2fb70/cenc.mpd",
        "kid": "1779c27b9d077a3ba0c9cc1bb9a94b9f",
        "key": "cc5cf3b7928fb9e0a1ee6a8b566f0a8e"
    },
    "bein2aus": {
        "url": "https://a122aivottlinear-a.akamaihd.net/OTTB/syd-nitro/live/clients/dash/enc/8m8cd46i1t/out/v1/83985c68e4174e90a58a1f2c024be4c9/cenc.mpd",
        "kid": "0b42be2664d7e811d04f3e504e0924c5",
        "key": "ae24090123b8c72ac5404dc152847cb8"
    },
    "skynz1": {
        "url": "https://dice-live-oc.akamaized.net/hdntl=exp=1764922569~acl=%2f*~id=1b4e7caa-e6c0-4402-85ab-5f15d41e9aa0~data=hdntl,dWlkPTU3MjQwMXxkY2Uuc2t5bnomaXA9NDkuMjI1LjEzNi4xODQmZXhwPTE3NjQ5MjI1OTgmZWlkPTI5NDkyMSZjaWQ9ZGNlLnNreW56Jm9pZD0zMTgmdHlwZT1MSVZF~hmac=89e78f814e690c5c3164c3b59f90650503964ddf81c925e2ee2232a1f41af506/dash/live/2093671/294921-311597/manifest-d.mpd",
        "kid": "4d346b1d1ae64d4a800409cffa14983e",
        "key": "208c972bd2da4359ac94e6944fe378b6"
    },
    "mlive5": {
        "url": "https://tglmp04.akamaized.net/out/v1/400fc0702dee453bb33ebcc29466e58a/manifest.mpd",
        "kid": "91b9592c819246c68b3b08a1fe08ba22",
        "key": "fa0d80dfd865b34077bae44cd4a0c5e6"
    },
    "fancodebd": {
        "url": "https://a166aivottlinear-a.akamaihd.net/OTTB/sin-nitro/live/clients/dash/enc/inpyms8ezu/out/v1/1084d5c9a97a4c5b9f9554c88f486646/cenc.mpd",
        "kid": "065051b99bf5cf8d9a3bde5cbde6aaf9",
        "key": "214bd176832872339ce184338320f9a2"
    },
    "skylaliga": {
        "url": "https://zap-live1-ott.izzigo.tv/2/out/u/dash/SKYSPORTS16HD/manifest.mpd",
        "kid": "c88dc6c668cac3b468d4a4c7e176ff3d",
        "key": "1aeb739de2c14ed0ad658ca8043208d8"
    },
    "laligatv": {
        "url": "https://a166aivottlinear-a.akamaihd.net/OTTB/dub-nitro/live/clients/dash/enc/k0duzgfejg/out/v1/70a50b1bda944628b8e7e66ab4069419/cenc.mpd",
        "kid": "620e51b82596475517a27aa425c52280",
        "key": "2b9ba811e9c5aeafc8ae1b71cdca4d6a"
    },
    "skypl": {
        "url": "https://a151aivottlinear-a.akamaihd.net/OTTB/lhr-nitro/live/clients/dash/enc/9o6jmlyjpm/out/v1/ad80a9bfecc6438f82f2af41c58d7fb8/cenc.mpd",
        "kid": "ca4316630f56d6f33e9ff73b7ad211d1",
        "key": "72c54e5646055f444e99bc1123919e89"
    },
    "bt1": {
        "url": "https://a122aivottlinear-a.akamaihd.net/OTTB/bom-nitro/live/dash/enc/wf8usag51e/out/v1/bd3b0c314fff4bb1ab4693358f3cd2d3/cenc.mpd",
        "kid": "d0f2e5c39e70c18f29bf77768a1ad89a",
        "key": "d6853c51fcf37a18905f0609972395d7"
    },
    "bt2": {
        "url": "https://a122aivottlinear-a.akamaihd.net/OTTB/bom-nitro/live/dash/enc/f0qvkrra8j/out/v1/f8fa17f087564f51aa4d5c700be43ec4/cenc.mpd",
        "kid": "9f51f3dc6313ac8bc668e2d9d1c04dfa",
        "key": "74bc63e5a193454a91ca494975db33f9"
    },
    "bt3": {
        "url": "https://a129aivottlinear-a.akamaihd.net/OTTB/bom-nitro/live/dash/enc/lsdasbvglv/out/v1/bb548a3626cd4708afbb94a58d71dce9/cenc.mpd",
        "kid": "a93c1cbfdccd23233bac13540c693e7f",
        "key": "2f6ab2e6693eb847eff3c9da8f9d01fc"
    },
    "bt4": {
        "url": "https://a129aivottlinear-a.akamaihd.net/OTTB/bom-nitro/live/dash/enc/i2pcjr4pe5/out/v1/912e9db56d75403b8a9ac0a719110f36/cenc.mpd",
        "kid": "192b1115da041585c77200128549efa1",
        "key": "634e10efe4abbb14be400a3ccbac0258"
    },
    "tsn1": {
        "url": "https://otte.live.fly.ww.aiv-cdn.net/pdx-nitro/live/clients/dash/enc/u142pfptsm/out/v1/1caa3b2dfa9e448d8f61209bdfc1acdc/cenc.mpd",
        "kid": "7e99f734748d098cbfa2f7bde968dd44",
        "key": "98ea6088c3222e9abaf61e537804d6cc"
    },
    "tsn2": {
        "url": "https://otte.live.fly.ww.aiv-cdn.net/pdx-nitro/live/clients/dash/enc/v5v9yfn62i/out/v1/0991e33d09da46b2857fcc845db95c40/cenc.mpd",
        "kid": "362202eefc5d9e42eec6450998cce9e8",
        "key": "978dfdd53186ec587d940e0bd1e2ec42"
    },
    "tsn3": {
        "url": "https://otte.live.fly.ww.aiv-cdn.net/pdx-nitro/live/clients/dash/enc/mrskysvotx/out/v1/ad58961bd8fd48d2944e461c034b8914/cenc.mpd",
        "kid": "d9097a1b7d04b7786b29f2b0e155316d",
        "key": "279695ebe0fb1bc5787422b6b59ce8a8"
    },
    "ziggo5": {
        "url": "https://mag04.tvx.prd.tv.odido.nl/wh7f454c46tw865586829_-819821292/PLTV/86/224/3221241610/3221241610.mpd?accountinfo=~~V2.0~LNS2PBO5tyhp5z1Pe6ObBA6cd7a4ec35c4492167b9376e6dff2932~BZw2dESHw-I1PQCFh9gGxCMvrIIzgMdYAe900qj8l6aoXUX9ahyR6I9EUIu7nDR4f4887615c83ea7a8cee6dd33137c4ebe:UTC,",
        "kid": "3fb40d85724942f994d86943f48021db",
        "key": "a6da8742502c8a2153067f5f2a70fb02"
    },
    "fancode": {
        "url": "https://a204aivottepl-a.akamaihd.net/sin-nitro/live/clients/dash/enc/fdb3pubmek/out/v1/aefca6420f944a9482e117f315de535f/cenc.mpd",
        "kid": "7e9239c1982d984a002df3ed049d0756",
        "key": "1b8a17598129a3618535c8fb05f103fe"
    },
    "ziggo6": {
        "url": "https://mag03.tvx.prd.tv.odido.nl/wh7f454c46tw1024019879_757686866/PLTV/86/224/3221241521/3221241521.mpd?accountinfo=~~V2.0~URnD_afuosWHfY5OEqRXOwfa01c8ac56cf4511de39c2c4a3cab278~iVxKjbtf2gx_dYFqI-vt5C4Cu3COYDjZaw6C_kO2T2wm30fwo1ctD1gr_e2PrgTh48867c3177f3c34842031623cb2e06c9:UTC, ",
        "kid": "1a0ffa532aa2498490826e2f6a37f7c9",
        "key": "a8cec27bc7d47909c5b0d8f473b43e8d"
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
