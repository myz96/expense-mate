const submitSignUpForm = () => {
    let form = document.querySelector("#sign_up_form")
    form.submit()
}

const submitLoginForm = () => {
    let form = document.querySelector("#login_form")
    form.submit()
}

const submitCreatePost = () => {
    let form = document.querySelector("#create_post_form")
    form.submit()
}

const submitAddTransactionForm = () => {
    let form = document.querySelector("#transaction_form")
    form.submit()
}

const submitEditTransactionForm = () => {
    let form = document.querySelector("#edit_transaction_form")
    form.submit()
}

const submitSettingsForm = () => {
    let form = document.querySelector("#settings_form")
    form.submit()
}

const submitComment = (e) => {
    if (e.keyCode === 13) {
        let form = document.querySelector("#add_comment_form")
        form.submit()
    }
}