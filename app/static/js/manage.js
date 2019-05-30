// function delLi()
// {
//     var delbtn = document.getElementsByClassName('del');
//
//     for(i = 0;i<delbtn.length;i++)
//     {
//         delbtn[i].onclick = function () {
//
//             var Li = this.parentNode.parentNode
//             var alpha = 100;
//             var iHeight = oParent.offsetHeight;
//             timer = setInterval(function () {
//                 css(oParent, "opacity", (alpha -= 10));
//                 if (alpha < 0) {
//                     clearInterval(timer);
//                     timer = setInterval(function () {
//                         iHeight -= 10;
//                         iHeight < 0 && (iHeight = 0);
//                         css(oParent, "height", iHeight + "px");
//                         iHeight == 0 && (clearInterval(timer), oUl.removeChild(oParent))
//                     }, 30)
//                 }
//             }, 30);
//             this.onclick = null
//         }
//     }
// }

// delLi()