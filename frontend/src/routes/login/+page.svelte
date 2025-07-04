<script lang="ts">
    import { enhance } from '$app/forms';
    let showPassword = false;
</script>

<svelte:head>
    <title>Login - Shorklights</title>
</svelte:head>
<section class="tall:fixed tall:inset-0 h-screen flex flex-col items-center justify-center">
    <img class="h-32 w-32 z-[1]" src="/logo.png" alt="Logo" />
    <form method="POST" use:enhance>
        <div class="flex flex-col items-center justify-center p-6 m-4 bg-gray-900 rounded-lg border-2 border-sky-400/90 shadow-[0_0_102px_4px] shadow-sky-400/90">
            <h1 class="font-bold text-2xl"><span class='text-sky-400'>Shork</span>lights</h1>
            <div class="flex flex-col w-64 mt-4">
                <input type="text" placeholder="Username" name="username" class="mb-4 p-2 border border-gray-600 rounded bg-gray-800" />
                <div class="relative">
                    <input type={showPassword ? 'text' : 'password'} placeholder="Password" name="password" class="mb-4 p-2 border border-gray-600 rounded bg-gray-800 w-full pr-10"/>
                    <button type="button" class="absolute text-xl right-2 top-[0.65rem] text-gray-400" on:click={() =>{  return showPassword = !showPassword; }} tabindex="-1">
                        <span class={showPassword ? 'icon-[iconamoon--eye-off]': 'icon-[iconamoon--eye]'}></span>
                    </button>
                </div>
            </div>
            <button class="bg-sky-400 text-white px-4 py-2 rounded cursor-pointer hover:bg-sky-600 transition duration-200">Login</button>
        </div>
    </form>
</section>