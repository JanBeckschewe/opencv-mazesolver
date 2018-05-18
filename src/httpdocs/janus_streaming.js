let streaming;
document.addEventListener('DOMContentLoaded', () => {
    Janus.init({
        debug: true,
        dependencies: Janus.useDefaultDependencies(),
        callback: function () {
            let janus = new Janus({
                server: '/janus_rest',
                success: () => {
                    janus.attach({
                        plugin: "janus.plugin.streaming",
                        success: (pluginHandle) => {
                            streaming = pluginHandle;
                            const body = {"request": "list"};
                            Janus.debug("Sending message (" + JSON.stringify(body) + ")");
                            streaming.send({
                                "message": body,
                                success: (result) => {
                                    console.log("onlist", result);
                                    if (result.list.length > 0) {
                                        const body = {"request": "watch", id: result.list[0].id};
                                        streaming.send({
                                            "message": body,
                                            success: () => {
                                                console.log("on watchrequest success", result)
                                            }
                                        });
                                    }
                                }
                            });
                        },
                        onmessage: (msg, jsep) => {
                            console.log("message: ", msg, jsep);
                            if (jsep) {
                                streaming.createOffer({
                                    jsep: jsep,
                                    media: {videoSend: false, audioSend: false},
                                    success: (ourjsep) => {
                                        console.log("onmessageSuccess", ourjsep);
                                        const body = {"request": "start"};
                                        streaming.send({"message": body, "jsep": ourjsep});
                                    }
                                })
                            }
                        },
                        onremotestream: (stream) => {
                            console.log("onremotestream");
                            Janus.attachMediaStream(document.getElementById("janus_stream"), stream);
                        }
                    });
                }
            });
        }
    });
});
