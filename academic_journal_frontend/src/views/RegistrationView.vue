<template>
    <h1>Регистрация</h1>
    <div>
        <div>
            <p>
                Фамилия:
                <br>
                <input id="last_name" type="text" maxlength="40" v-model="last_name">
            </p>
            <p>
                Имя:
                <br>
                <input id="fitst_name" type="text" maxlength="40" v-model="first_name">
            </p>
            <p>
                Email:
                <br>
                <input id="email" type="text" maxlength="40" v-model="email">
            </p>
            <p>
                Логин (юзернейм):
                <br>
                <input id="login" type="text" maxlength="15" v-model="username">
            </p>
            <p>
                Пароль:
                <br>
                <input id="password" type="password" maxlength="40" v-model="password">
            </p>
        </div>
    </div>
    <button class="default-button auth-button" @click="registrationAccountMethod">Зарегистрироваться</button>
</template>

<script>
import { registrationAccount } from '@/network';
import { tokenIsSet } from '@/service';
import router from '@/router';

export default{
    data() {
        return {
            username: "",
            last_name: "",
            first_name: "",
            password: "",
            email: ""
        };
    },
    methods: {
        async registrationAccountMethod() {
            await registrationAccount(
                this.username, 
                this.last_name, 
                this.first_name, 
                this.password,
                this.email
            );
        }
    },
    mounted() {
        if (tokenIsSet()) {
            router.replace({ path: '/' });
        }
    }
}
</script>