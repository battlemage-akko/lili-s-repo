var danmulistbtn = document.querySelector('.danmubtn')
var danmu = document.querySelector(".danmuholder")
var video = document.querySelector('.thisvideo')
var danmulist = document.querySelector('.danmulist')
var danmuflag = 0
danmulistbtn.addEventListener("click", (e) => {
    danmulistbtn.classList.toggle("active")
    if (!danmuflag) {
        danmu.style.height = video.clientHeight + 100 +'px'
        danmuflag = 1
        danmulist.style.height = video.clientHeight + 100 + 'px'
    } else {
        danmuflag = 0
        danmu.style.height = 50 + 'px'
    }
})