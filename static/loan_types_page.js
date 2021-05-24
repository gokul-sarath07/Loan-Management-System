document.querySelector(".add_loan_type").onclick = () => {
    document.querySelector(".loan_types_form_container").style.cssText = "opacity: 1; visibility: visible";
}

document.querySelector(".loan_types_form_cancel_btn").onclick = () => {
    document.querySelector(".loan_types_form_container").style.cssText = "opacity: 0; visibility: hidden";
}
