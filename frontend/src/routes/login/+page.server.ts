import type { Actions } from './$types';
import { redirect } from '@sveltejs/kit';
const ACCESS_TOKEN_EXPIRE_MINUTES = 60;

export const actions = {
    default: async ({ cookies, fetch, request }) => {
        const formData = await request.formData();
        const username = formData.get('username') as string;
        const password = formData.get('password') as string;

        if (!username || !password) { return { error: 'Username and password are required' }; }

        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ username, password }).toString(),
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log('Login successful:', responseData);
            cookies.set('token', responseData.data.access_token, {
                path: '/',
                httpOnly: false,
                sameSite: 'lax',
                secure: false,
                maxAge: ACCESS_TOKEN_EXPIRE_MINUTES * 60, // Convert minutes to seconds
            });
            throw redirect(303, '/')
        } else {
            throw 'Login failed';
        }
    }
} satisfies Actions;