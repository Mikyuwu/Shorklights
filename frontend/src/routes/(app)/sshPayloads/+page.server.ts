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
    },

    executePayload: async ({ cookies, fetch, request }) => {
        const token = AuthHelper.getToken(cookies);
        if (!token) {
            return { error: 'Unauthorized' };
        }

        const formData = await request.formData();

        formData.forEach((value, key) => {
            if (value && typeof value === 'object' && 'name' in value && 'type' in value && 'size' in value) {
                console.log('file', key, value.name, value.type, value.size);
            } else {
                console.log(key, value);
            }
        });

        let url: string;
        switch (formData.get("payloadType")) {
            case 'changeWallpaper':
                url = "/api/sshPayloads/changeWallpaper";
                break;
            case 'playSounds':
                url = "/api/sshPayloads/playSounds";
                break;
            default:
                return { error: 'Invalid payload type' };
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
            },
            body: formData
        })

        const data = await response.json();
        console.log(data);
    }
}