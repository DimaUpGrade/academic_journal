import axios from 'axios';
import router from '../router';
import swal from 'sweetalert';
import { tokenIsSet } from '../service';


// In Docker-container
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
            localStorage.setItem("last_name", response.data['last_name']);
            localStorage.setItem("first_name", response.data['first_name']);
            router.back();
        })
        .catch((error) => {
            defaultErrorHandler()
            // swal('ошибка')
            // console.log(error);
        });
}


async function registrationAccount(username_, last_name_, first_name_, password_, email_) {
    let result;
    result = await axios({
        method: 'post',
        url: `${API_URL}/api/registration/`,
        headers: {},
        data: {
            username: username_,
            last_name: last_name_,
            first_name: first_name_,
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
            swal({
                title: "Успешный выход!",
                text: "Вы вышли из аккаунта!",
                type: "success"
            }).then(function () {
                localStorage.removeItem("token");
                localStorage.removeItem("username");
                localStorage.removeItem("last_name");
                localStorage.removeItem("first_name");
                router.go();
            });
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


async function getGroups() {
    let result;

    result = await axios({
        method: 'get',
        url: `${API_URL}/api/groups/`,
    })
        .then(response => result = response)
        .catch((error) => {
            swal(error.response.status);
        })

    return result.data;
}


async function getSemesters() {
    let result;

    result = await axios({
        method: 'get',
        url: `${API_URL}/api/semesters/`,
    })
        .then(response => result = response)
        .catch((error) => {
            swal(error.response.status);
        })

    return result.data;
}


async function getSubjects() {
    let result;
    if (tokenIsSet()) {
        result = await axios({
            method: 'get',
            url: `${API_URL}/api/subjects/`,
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("token")
            }
        })
            .then(response => result = response)
            .catch((error) => {
                swal(error.response.status);
            })
    }
    else {
        result.data = {}
    }
    return result.data;
}


async function getLessons(group, subject, semester_id) {
    let result;
    if (tokenIsSet()) {
        result = await axios({
            method: 'get',
            url: `${API_URL}/api/lessons/?group=${group}&subject=${subject}&semester=${semester_id}`,
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("token")
            }
        })
            .then(response => result = response)
            .catch((error) => {
                swal(error.response.status);
            })
    }
    else {
        result.data = {}
    }
    return result.data;
}


async function getRanksForLesson(lesson_id) {
    let result;
        result = await axios({
            method: 'get',
            url: `${API_URL}/api/ranks/?lesson_id=${lesson_id}`,
        })
            .then(response => result = response)
            .catch((error) => {
                swal(error.response.status);
            })

    return result.data;
}


async function getStudentsByGroup(group_title) {
    let result;
        result = await axios({
            method: 'get',
            url: `${API_URL}/api/students/?group_title=${group_title}`,
        })
            .then(response => result = response)
            .catch((error) => {
                swal(error.response.status);
            })

    return result.data;
}


async function createLesson(date_, order_in_day_, group_, subject_, semester_id_) {
    let result;

    result = await axios({
        method: 'post',
        url: `${API_URL}/api/lessons/`,
        headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
        },
        data: {
            date: date_,
            order_in_day: order_in_day_,
            group: group_,
            subject: subject_,
            semester_id: semester_id_
        }
    })
        .then((obj_) => {
            swal({
                title: "Занятие создано!",
                text: 'Вы будете перенаправлены на страницу занятия!',
                type: "success"
            }).then(function () {
                router.push(`/lessons/${obj_.data.lesson_id}`);
            });
        })
        .catch((error) => {
            if (error.status == 400) {
                alert(Object.keys(error.response));
                swal({
                    title: "Занятие уже существует!",
                    text: "Вы будете перенаправлены на страницу занятия!",
                    type: "success"
                }).then(function () {
                    router.push(`/lessons/${error.response.data.lesson_id}`);
                });
            }
            
        });
}


async function getLesson(id) {
    let result;

    result = await axios({
        method: 'get',
        url: `${API_URL}/api/lessons/${id}/`,
        headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
        },
    })
    .catch((error) => {
        defaultErrorHandler()
    });

    return result.data;
}


async function postRanks(ranks) {
    let result;

    result = await axios({
        method: 'post',
        url: `${API_URL}/api/ranks/`,
        headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
        },
        data: {
            ranks,
        }
    })
    .catch((error) => {
        defaultErrorHandler()
    });
}


async function postVisits(visits_, id) {
    let result;

    result = await axios({
        method: 'patch',
        url: `${API_URL}/api/lessons/${visits_, id}/`,
        headers: {
            'Authorization': 'Token ' + localStorage.getItem("token")
        },
        data: {
            visits: visits_
        }
    })
    .catch((error) => {
        defaultErrorHandler()
    });
}


export {
    API_URL,
    axios,
    loginAccount,
    registrationAccount,
    logout,
    getGroups,
    getSubjects,
    getSemesters,
    getLessons,
    createLesson,
    getRanksForLesson,
    getStudentsByGroup,
    getLesson,
    postRanks,
    postVisits
}