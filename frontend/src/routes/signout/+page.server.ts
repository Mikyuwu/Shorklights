import { AuthHelper } from "$lib/authHelper";

export const load = async ({ cookies }) => {
    await AuthHelper.logout(cookies);
}
