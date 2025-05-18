import type { Actions } from './$types';

export const actions = {
    default: async ({ cookies, fetch, request }) => {
        const formData = await request.formData();
        const email = formData.get('email');
        const password = formData.get('password');

        const response = await fetch('/api/servers/getServers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
    }
} satisfies Actions;