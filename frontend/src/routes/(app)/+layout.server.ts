import { AuthHelper } from "$lib/authHelper";

export const load = async ({ cookies }) => {
    try {
        const tokenAuth = await AuthHelper.verifyAuth(cookies);
        if (tokenAuth) {
            const username = tokenAuth.username;
            return { username };
        } else {
            throw 'Token verification failed';
        }
    } catch (error) {
        await AuthHelper.logout(cookies);
    }
}

