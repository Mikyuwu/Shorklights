<script lang="ts">
    import { enhance } from '$app/forms';
    let showServerModal = false;
    let servers = [];
    let requestWaiting = false;

    function openServerModal() {
        showServerModal = true;
        requestWaiting = true;
    }
</script>

<section id="header" class="relative flex flex-col items-center z-20">
    <h1 class="text-4xl md:text-5xl font-bold text-center">
        <span class="text-sky-400">S</span>S<span class="text-sky-400">H</span>
    </h1>
    <div class="mt-1">
        <form method="POST" action="?/getServers" use:enhance={({ formElement, formData, action, cancel }) => {
            return ({ result }) => {
                console.log(result)
            }
        }}>
            <button type="submit" class="text-md md:text-xl flex items-center text-white font-semibold hover:text-sky-300 cursor-pointer transition" on:click={openServerModal}>
                <i class="icon-[iconamoon--arrow-right-2-bold] text-xl"></i>
                Select servers
            </button>
        </form>
    </div>
</section>
<section class="tall:fixed tall:inset-0 flex items-center justify-center z-0 mt-8">
    <section id="body">
        <article class="flex flex-wrap justify-center gap-12">
            <div class="flex flex-col items-center justify-center w-full max-w-xs md:w-72 m-2 h-56 bg-gray-900 rounded-lg border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 cursor-pointer hover:bg-gray-800 transition duration-200">
                <i class="icon-[iconamoon--folder-image] text-6xl text-sky-400 drop-shadow"></i>
                <p class="font-semibold text-lg text-center">Change wallpaper</p>
            </div>
            <div class="flex flex-col items-center justify-center w-full max-w-xs md:w-72 m-2 h-56 bg-gray-900 rounded-lg border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 cursor-pointer hover:bg-gray-800 transition duration-200">
                <i class="icon-[iconamoon--music-2] text-6xl text-sky-400 drop-shadow"></i>
                <p class="font-semibold text-lg text-center">Play sounds</p>
            </div>
        </article>
    </section>
</section>

{#if showServerModal}
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-8 rounded-lg border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 max-w-sm w-full relative">
            <button class="absolute top-2 right-2 text-sky-400 text-2xl cursor-pointer hover:text-red-500 transition duration-200" on:click={() => showServerModal = false}>&times;</button>
            <h2 class="text-xl font-bold mb-4">Popup Title</h2>
            <p>This is your popup content.</p>
        </div>
    </div>
{/if}