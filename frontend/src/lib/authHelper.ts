import { redirect } from '@sveltejs/kit';
import { JWT_SECRET_KEY } from '$env/static/private';
import jwt from 'jsonwebtoken';

export class AuthHelper {
    private static getToken(cookies: { get: (name: string) => string | undefined }): string | undefined {
        return cookies.get('token');
    }

    public static async verifyAuth(cookies: { get: (name: string) => string | undefined }): Promise<{ username: string } | false> {
        try {
            const token = this.getToken(cookies);
            if (!token) { throw 'No token found'; }

            const tokenPayload = jwt.verify(token, JWT_SECRET_KEY, function (err, decoded) {
                if (err) {
                    throw 'Token invalid';
                    return false;
                }
                console.log(decoded);
                return decoded;
            })
            const username = tokenPayload.sub || "Unknown";

            const currentTime = Math.floor(Date.now() / 1000);
            if (tokenPayload.exp < currentTime) { throw 'Token expired'; }

            return { username };
        } catch (error) {
            console.error('Token verification failed:', error);
            return false;
        }
    }

    public static async logout(cookies: { delete: (name: string) => void }): Promise<void> {
        cookies.delete('token', { path: '/' });
        throw redirect(303, '/login');
    }
}