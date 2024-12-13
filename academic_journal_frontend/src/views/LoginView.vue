<template>
    <h1>Авторизация</h1>
    <div>
        <div>
            <p>
                Логин: <input id="login" type="text" maxlength="15" v-model="login">
            </p>
            <p>
                Пароль: <input id="password" type="password" maxlength="40" v-model="password">
            </p>
        </div>
    </div>
    <button class="default-button auth-button" @click="loginAccountMethod">Войти</button>
</template>

<script>
import { loginAccount } from '@/network';
import { tokenIsSet } from '@/service';
import router from '@/router';

export default{
    data() {
        return {
            login: "",
            password: ""
        };
    },
    methods: {
        async loginAccountMethod() {
            await loginAccount(this.login, this.password);
        }
    },
    mounted() {
        if (tokenIsSet()) {
            router.replace({ path: '/' });
        }
    }
}
</script>