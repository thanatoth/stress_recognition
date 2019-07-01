//動画流す準備
var video = document.getElementById("video");
// getUserMedia によるカメラ映像の取得
var media = navigator.mediaDevices.getUserMedia({
    video: true,//ビデオを取得する
    audio: false,//音声が必要な場合はture
});
//リアルタイムに再生（ストリーミング）させるためにビデオタグに流し込む
media.then((stream) => {
    video.srcObject = stream;
});

function snapshot() {
    let videoElement = document.querySelector('video');
    let canvasElement = document.querySelector('canvas');
    let context = canvasElement.getContext('2d');

    context.drawImage(videoElement, 0, 0, videoElement.width, videoElement.height);
    let base64 = canvasElement.toDataURL('image/png');
    document.querySelector('img').src = base64;

    //let canvas = document.querySelector('canvas')
    let link = document.getElementById('hiddenLink')
    link.href = canvasElement.toDataURL()
    document.getElementById('canvasImage').src = canvasElement.toDataURL()
    link.click()
/*
    //var base64 = this.canvas.toDataURL('image/png');
    var request = {
      url: 'http://www.wakuwaku-caffein.tk/api/predict/base64',
      method: 'POST',
      params: {
        image: base64.replace(/^.*,/, '')
      },
      success: function (response) {
        console.log(response.responseText);
      }
    };
    Ext.Ajax.request(request);
    */
/*
    var sendImage = function (evt) {
        var canvas = document.getElementById("canvas");
        var data = canvas.toDataURL();
        data = data.replace('data:image/png;base64,', '');
        $('<form/>', {action: 'http://www.wakuwaku-caffein.tk/api/predict/', method: 'post'})
                .append($('<input/>', {type: 'hidden', name: 'image', value: data}))
                .appendTo(document.body)
                .submit();
    };
    $('#send').bind('click', sendImage);
    */

    const FormData = require('form-data');
    const fs = require('fs');
    const form = new FormData();
    form.append('image', fs.createReadStream('/Users/satokanako/Downloads/canvas.png'));
    form.submit('http://www.wakuwaku-caffein.tk/api/predict/', function(err, res) {
      console.log(res.statusCode);
    });

}
