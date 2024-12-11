import axios from 'axios';
import router from '../router';
import swal from 'sweetalert';
import { tokenIsSet } from '../service';


const API_URL = "http://localhost:10000";

function defaultErrorHandler() {
    swal({
        title: "Ошибка!",
        text: "Что-то пошло не так...",
        type: "success"
    }).then(function () {

    });
}


async function loginAccount(username_, password_) {
    let result;
    result = await axios({
        method: 'post',
        url: `${API_URL}/api/login/`,
        headers: {},
        data: {
            username: username_,
            password: password_
        }
    })
        .then((response) => {
            localStorage.setItem("token", response.data['Token']);
            localStorage.setItem("username", username_);
            router.back();
        })
        .catch((error) => {
            defaultErrorHandler()
            // swal('ошибка')
            // console.log(error);
        });
}


// WIP
async function registrationAccount(username_, password_, email_) {
    let result;
    result = await axios({
        method: 'post',
        url: `${API_URL}/api/registration/`,
        headers: {},
        data: {
            username: username_,
            password: password_,
            email: email_
        }
    })
        .then(async (response) => {
            await loginAccount(username_, password_);
        })
        .catch((error) => {
            defaultErrorHandler()
            // console.log(error);
        });
}


async function logout() {
    let result;

    result = await axios({
        method: 'post',
        url: `${API_URL}/api/logout/`,
        headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
        }
    })
        .then((response) => {
            // delete this
            swal({
                title: "Успешный выход!",
                text: "Вы вышли из аккаунта!",
                type: "success"
            }).then(function () {
                localStorage.removeItem("token");
                localStorage.removeItem("username");
                router.go();
            });
            // alert("Успешный выход!");

        })
        .catch((error) => {
            if (error) {
                swal({
                    title: "Произошла ошибка!",
                    text: "Что-то пошло не так...",
                    type: "success"
                }).then(function () {
                    router.push({ path: '/' });
                });
            }
        })
}