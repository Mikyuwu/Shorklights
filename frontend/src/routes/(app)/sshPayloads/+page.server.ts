import type { Actions } from './$types';
import {AuthHelper} from "$lib/authHelper";

export const actions = {
    getServers: async ({ cookies, fetch, request }) => {
        const token = AuthHelper.getToken(cookies);
        if (!token) {
            return { error: 'Unauthorized' };
        }
        const response = await fetch('/api/servers/getServers', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token,
            }
        });

        if (response.ok) {
            const data = await response.json();
            return { servers: data.data };
        } else {
            return { error: 'Failed to fetch servers' };
        }
    }
}