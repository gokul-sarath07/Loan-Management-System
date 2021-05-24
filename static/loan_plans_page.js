document.querySelector(".add_loan_plan").onclick = () => {
    document.querySelector(".loan_plans_form_container").style.cssText = "opacity: 1; visibility: visible";
}

document.querySelector(".loan_plan_form_cancel_btn").onclick = () => {
    document.querySelector(".loan_plans_form_container").style.cssText = "opacity: 0; visibility: hidden";
}
