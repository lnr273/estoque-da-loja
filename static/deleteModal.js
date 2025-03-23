let btns = document.querySelectorAll("#deleteBtn")

if (btns) {
    for (let i = 0; i < btns.length; i++) {
        btns[i].addEventListener("click", () => {

            let modal = document.querySelector(".modal")
            modal.style.visibility = "visible"
            
            let confirmBtn = document.querySelector("#confirm")
            let cancelBtn = document.querySelector("#cancel")
            let forms = document.querySelectorAll("#deleteForm")
            
            confirmBtn.addEventListener("click", () => {
                forms[i].submit()
                modal.style.visibility = "hidden"
            })

            cancelBtn.addEventListener("click", () => {
                modal.style.visibility = "hidden"
            })
        })
    }
}
