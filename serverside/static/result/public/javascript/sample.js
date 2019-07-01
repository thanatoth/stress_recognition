// alert("Hello");
let img = new Array("1.png","2.png");
let status1,status2;
judge();

//1秒ごとに画像を切り替え
function judge(){
  console.log(status1);
  // -------------
  //get　に書き換える！！
  if(status1==1) {status1=0;}
  else {status1=1;}

  if(status2==1) {status2=0;}
  else {status2=1;}
  // -------------

  // 画像を変える
  img_change(status1,status2);

  setTimeout("judge()",1000); //1秒毎にジャッジ

}

function img_change(in_status1,in_status2){
  document.getElementById("person1").src = img[in_status1];
  document.getElementById("person2").src = img[in_status2];
}
