var newSS, styles="\
body { background: #8b754f url(http://staremapy.mzk.cz/img/body-bg-100.jpg) repeat-y center top; }\
h1 { color: #4b3611; font: normal normal 225% Georgia, Times New Roman,sans-serif; border: none; background: none; margin: 0;  }\
#header { border: none; background-color: transparent; margin: 0; }\
p.description { background: transparent url(http://staremapy.mzk.cz/img/divider.gif) no-repeat 0px 20px; margin: 0; padding-top: 30px; border: none; }\
#header div.wrapper { background: transparent url(http://staremapy.mzk.cz/img/h1-plain-100.jpg) no-repeat top left; min-height: 113px; }\
#container { background: transparent url(http://staremapy.mzk.cz/img/text-bg-100.jpg) no-repeat 0px 113px; }\
#footer { background: transparent url(http://staremapy.mzk.cz/img/star.gif) no-repeat 500px 0px; height: 140px; border: 0px; color: #B4543D; font-size: x-small; }\
";

if(document.createStyleSheet) {
    document.createStyleSheet("javascript:'"+styles+"'"); 
} else {
    newSS=document.createElement('link'); 
    newSS.rel='stylesheet';  
    newSS.href='data:text/css,' + escape(styles);
    document.getElementsByTagName("head")[0].appendChild(newSS); 
}
