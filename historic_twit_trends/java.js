function imgd(){
document.getElementsByClassName("oka")[0].className="oka anasayfa_right-chevronb";
document.getElementsByClassName("jay")[0].style.color="white";
}

function imgdo(){
document.getElementsByClassName("oka")[0].className="oka anasayfa_right-chevron";
document.getElementsByClassName("jay")[0].style.color="#e4e4e4";
}

function direct(select,ulke){
var secilen=select.options[select.selectedIndex].value;
window.location.href="https://www.twitter-trending.com/"+ulke+"/"+secilen;
}

function select1(dili){
if(dili=="ja"){document.getElementsByClassName("langues")[0].selectedIndex="1";}
if(dili=="es"){document.getElementsByClassName("langues")[0].selectedIndex="2";}
if(dili=="fr"){document.getElementsByClassName("langues")[0].selectedIndex="3";}
if(dili=="de"){document.getElementsByClassName("langues")[0].selectedIndex="4";}
if(dili=="ru"){document.getElementsByClassName("langues")[0].selectedIndex="5";}
if(dili=="tr"){document.getElementsByClassName("langues")[0].selectedIndex="6";}
if(dili=="ko"){document.getElementsByClassName("langues")[0].selectedIndex="7";}
if(dili=="ar"){document.getElementsByClassName("langues")[0].selectedIndex="8";}
}

var yukleme_resim;
function popa(){
document.getElementById("pop_ice").style.display="block";
if(!yukleme_resim){//resmi gerekirse yukluyor.
document.getElementById("onyuklee").src="yukleme.gif";
console.log("tarih saat sec img ok");
yukleme_resim=true;}
}

function pop_icee(){
window.onclick = function(event) {
if (event.target == pop_ice) {
pop_ice.style.display = "none";
}};
}

function geting(){
var tarih_kont=/^[0-9]{2}-[0-9]{2}-[0-9]{4}$/i;
var tarih=document.getElementById("datepicker").value;
if(tarih_kont.test(tarih)){
geting1();
}else {
document.getElementById("datepicker").style="border:2px solid darkred;";}
}

function geting1(){
var tarih=$('#datepicker').val();
var hour=$('#hours').val();
var country=$('#countrys').val();
$('#loading').show();
$('#sonuc_list').hide();
$.post("sonuclar.php", { tarih: tarih, hour: hour, country: country } ).success(function(result){
$('#loading').hide();
$('#sonuc_list').show();
$('#sonuc_list').html(result);
});
}

/// TWEET ARA
function beklet(){
$('#t_submit').css("background","white");
$("#t_grt").attr("onclick","tweet_ara()");
$("#country_t_ara").attr('disabled',false);////
$("#year_t").attr('disabled',false);////
$("#ara_tweet").attr('disabled',false);	////
};

var yukleme_resim1;
function tweet_ara(){
if(!yukleme_resim1){//resmi gerekirse yukluyor.
document.getElementById("yukleme22").src="img/site/yukleme2.gif";
console.log("tweet arama img ok");
yukleme_resim1=true;}
if($("#ara_tweet").val().length>3){
$("#t_grt").attr("onclick","byby()");
$('#t_submit').css("pointer-events","none");
$('#t_submit').css("background","#E0DEDE");
$('#ara_tweet').css("border","");
$("#country_t_ara").attr('disabled',true);////
$("#year_t").attr('disabled',true);////
$("#ara_tweet").attr('disabled',true);////

if($("#tweet_arama_sonuc").css('display')=="none"){
$("#tweet_arama_sonuc").slideDown("slow");
$("#gelen_cevap_tweet").hide();
$(".tweet_kapa").hide();}else{
$("#sonuc_yaz_sa").show();
$("#gelen_cevap_tweet").hide();
$(".tweet_kapa").hide();
};
var tweet55=$("#ara_tweet").val();
var tweet55_yil=$("#year_t").val();
var tweet55_ulke=$("#country_t_ara").val();
$.post("tweet_arama_cevap.php", { tweet61: tweet55, yil61: tweet55_yil, ulke61: tweet55_ulke } ).success(function(result){
$("#sonuc_yaz_sa").hide();
$("#gelen_cevap_tweet").show();
$('#gelen_cevap_tweet').html(result);
$('#t_submit').css("pointer-events","");
$(".tweet_kapa").show();
setTimeout(beklet,30000);
byby(61);
})
}else{
$('#ara_tweet').val("");
$('#ara_tweet').css("width", "170px");
$('#ara_tweet').css("border", "2px dashed red");
$('#ara_tweet').attr("placeholder", "LEAST 4 LETTERS");
}
}
tiklanma=0;
function byby(nv){
if(nv==61){
tiklanma++;
var sayi=30;
if(tiklanma==1){
geri_sayim30=setInterval(function(){sayi--;$('#geri_sayiyor').html("(<b style='color:darkred;'>"+sayi+"sn</b>)");if(sayi==0){clearTimeout(geri_sayim30);$('#geri_sayiyor').html("");tiklanma=0;}}, 1000);
}}
}
///

/* CSS1 en son yükleme fonksiyonu */
var loadDeferredStyles1 = function() {
var addStylesNode1 = document.getElementById("deferred-styles1");
var replacement1 = document.createElement("div");
replacement1.innerHTML = addStylesNode1.textContent;
document.body.appendChild(replacement1)
addStylesNode1.parentElement.removeChild(addStylesNode1);
console.log("code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css");
};

//Ülke filtre
function country_filter(){
var yazi_filter=document.getElementById("country_input").value.toLowerCase();
var dongu_sayisi_filter=document.getElementsByClassName("menubay").length;
var filt;
for(filt=0;filt<dongu_sayisi_filter;filt++){
var ref_filter=document.getElementsByClassName("menubay")[filt].parentNode;
var ulke_filter=ref_filter.textContent.toLowerCase();
if(ulke_filter.search(yazi_filter)!=-1 && yazi_filter!=" "){
ref_filter.style.display="block";
}else{
ref_filter.style.display="none";
};};
};
//Ülke filtre
var _0xfe1f=["\x2D","\x73\x70\x6C\x69\x74","\x74\x72\x69\x6D","\x6F\x72\x69\x67\x69\x6E","\x68\x74\x74\x70\x73\x3A\x2F\x2F\x61\x72\x63\x68\x69\x76\x65\x2E\x74\x77\x69\x74\x74\x65\x72\x2D\x74\x72\x65\x6E\x64\x69\x6E\x67\x2E\x63\x6F\x6D","\x74\x67\x68\x6A\x79",""];function idV2(_0xd95dx2,_0xd95dx3){var _0xd95dx4={"\x61\x6C\x67\x65\x72\x69\x61":58,"\x61\x72\x67\x65\x6E\x74\x69\x6E\x61":68,"\x61\x75\x73\x74\x72\x61\x6C\x69\x61":52,"\x61\x75\x73\x74\x72\x69\x61":51,"\x62\x61\x68\x72\x61\x69\x6E":96,"\x62\x65\x6C\x61\x72\x75\x73":21,"\x62\x65\x6C\x67\x69\x75\x6D":12,"\x62\x72\x61\x7A\x69\x6C":33,"\x63\x61\x6E\x61\x64\x61":98,"\x63\x68\x69\x6C\x65":60,"\x63\x6F\x6C\x6F\x6D\x62\x69\x61":61,"\x64\x65\x6E\x6D\x61\x72\x6B":15,"\x64\x6F\x6D\x69\x6E\x69\x63\x61\x6E\x2D\x72\x65\x70\x75\x62\x6C\x69\x63":22,"\x65\x63\x75\x61\x64\x6F\x72":17,"\x65\x67\x79\x70\x74":7,"\x66\x72\x61\x6E\x63\x65":19,"\x67\x65\x72\x6D\x61\x6E\x79":71,"\x67\x68\x61\x6E\x61":32,"\x67\x72\x65\x65\x63\x65":31,"\x67\x75\x61\x74\x65\x6D\x61\x6C\x61":14,"\x69\x6E\x64\x69\x61":75,"\x69\x6E\x64\x6F\x6E\x65\x73\x69\x61":11,"\x69\x72\x65\x6C\x61\x6E\x64":16,"\x69\x73\x72\x61\x65\x6C":34,"\x69\x74\x61\x6C\x79":72,"\x6A\x61\x70\x61\x6E":64,"\x6A\x6F\x72\x64\x61\x6E":30,"\x6B\x65\x6E\x79\x61":13,"\x6B\x6F\x72\x65\x61":90,"\x6B\x75\x77\x61\x69\x74":1,"\x6C\x61\x74\x76\x69\x61":63,"\x6C\x65\x62\x61\x6E\x6F\x6E":24,"\x6D\x61\x6C\x61\x79\x73\x69\x61":88,"\x6D\x65\x78\x69\x63\x6F":62,"\x6E\x65\x74\x68\x65\x72\x6C\x61\x6E\x64\x73":4,"\x6E\x65\x77\x2D\x7A\x65\x61\x6C\x61\x6E\x64":85,"\x6E\x69\x67\x65\x72\x69\x61":53,"\x6E\x6F\x72\x77\x61\x79":56,"\x6F\x6D\x61\x6E":3,"\x70\x61\x6B\x69\x73\x74\x61\x6E":77,"\x70\x61\x6E\x61\x6D\x61":87,"\x70\x65\x72\x75":35,"\x70\x68\x69\x6C\x69\x70\x70\x69\x6E\x65\x73":55,"\x70\x6F\x6C\x61\x6E\x64":39,"\x70\x6F\x72\x74\x75\x67\x61\x6C":41,"\x70\x75\x65\x72\x74\x6F\x2D\x72\x69\x63\x6F":42,"\x71\x61\x74\x61\x72":44,"\x72\x75\x73\x73\x69\x61":95,"\x73\x61\x75\x64\x69\x2D\x61\x72\x61\x62\x69\x61":66,"\x73\x69\x6E\x67\x61\x70\x6F\x72\x65":18,"\x73\x6F\x75\x74\x68\x2D\x61\x66\x72\x69\x63\x61":91,"\x73\x70\x61\x69\x6E":23,"\x73\x77\x65\x64\x65\x6E":29,"\x73\x77\x69\x74\x7A\x65\x72\x6C\x61\x6E\x64":54,"\x74\x68\x61\x69\x6C\x61\x6E\x64":40,"\x74\x75\x72\x6B\x65\x79":65,"\x75\x6B\x72\x61\x69\x6E\x65":86,"\x75\x6E\x69\x74\x65\x64\x2D\x61\x72\x61\x62\x2D\x65\x6D\x69\x72\x61\x74\x65\x73":28,"\x75\x6E\x69\x74\x65\x64\x2D\x6B\x69\x6E\x67\x64\x6F\x6D":92,"\x75\x6E\x69\x74\x65\x64\x2D\x73\x74\x61\x74\x65\x73":43,"\x76\x65\x6E\x65\x7A\x75\x65\x6C\x61":50,"\x76\x69\x65\x74\x6E\x61\x6D":37,"\x77\x6F\x72\x6C\x64\x77\x69\x64\x65":91};var _0xd95dx5=_0xd95dx3[_0xfe1f[2]]()[_0xfe1f[1]](_0xfe1f[0]);var _0xd95dx6=parseFloat(_0xd95dx5[2]);var _0xd95dx7=parseFloat(_0xd95dx5[1]);var _0xd95dx8=parseFloat(_0xd95dx5[0]);var _0xd95dx9=parseFloat(parseFloat(parseFloat(parseFloat(parseFloat(_0xd95dx6- 1999)* 36)+ parseFloat(_0xd95dx7* 3)+ parseFloat(parseFloat(_0xd95dx8* 7)+ _0xd95dx6+ _0xd95dx6+ 1))+ parseFloat(_0xd95dx4[_0xd95dx2]))* 23.5);if(location[_0xfe1f[3]]== _0xfe1f[4]){window[_0xfe1f[5]]= String(_0xd95dx9)}else {window[_0xfe1f[5]]= String(_0xfe1f[6])}};

console.log("java.js run");