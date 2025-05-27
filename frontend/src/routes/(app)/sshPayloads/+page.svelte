<script lang="ts">
    import { enhance } from '$app/forms';
    let showServerModal = false;
    let servers = [];
    let requestWaiting = false;

    function refreshServerList() {
        showServerModal = true;
        requestWaiting = true;
        return ({ result }) => {
            let data = result.data["servers"]
            try {
                const serversList = document.getElementById('server-list')
                if (serversList) {
                    serversList.innerHTML = '';
                    if (data && data && Array.isArray(data)) {
                        data.forEach(server => {
                            const onlineClass = server.status === "online" ? "text-sky-400" : "text-gray-400";
                            const onlineStatus = server.status === "online" ? '✿ Online' : '✿ Offline';

                            serversList.innerHTML += `
                            <label class="serverItem flex items-center cursor-pointer w-full p-2 rounded-md bg-gray-800 hover:bg-gray-700">
                                <input type="checkbox" class="mr-2 hidden" />
                                <span class="${onlineClass}">${onlineStatus}</span><span class="mx-2">|</span> ${server.name} (${server.ip})
                            </label>`
                        });
                    } else {
                        serversList.innerHTML = '<p class="text-gray-300">No servers found.</p>';
                    }
                }
            } catch (error) {
                console.error('Error refreshing server list:', error);
            } finally {
                requestWaiting = false;
            }
        }
    }
</script>

<section id="header" class="relative flex flex-col items-center z-20">
    <h1 class="text-4xl md:text-5xl font-bold text-center">
        <span class="text-sky-400">S</span>S<span class="text-sky-400">H</span>
    </h1>
    <div class="mt-1">
        <form method="POST" action="?/getServers" use:enhance={refreshServerList}>
            <button type="submit" class="text-md md:text-xl flex items-center text-white font-semibold hover:text-sky-300 cursor-pointer transition">
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
    <div class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-8 rounded-2xl border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 shadow-2xl max-w-md w-full relative">
            <div class="flex items-center gap-4 mb-4">
                <input class="w-full border border-gray-700 bg-gray-800 text-white p-2 rounded-md" placeholder="Search servers..."/>
                <button class="text-sky-400 text-3xl font-bold hover:text-red-500 transition cursor-pointer duration-200" aria-label="Close" on:click={() => showServerModal = false}>&times;</button>
            </div>
            <div id="server-list" class="flex flex-col items-center justify-center gap-2 min-h-2">
                {#if requestWaiting}
                    <div class="loader"></div>
                {:else if servers.length === 0}
                    <p class="text-gray-300 text-center">No servers available.</p>
                {/if}
            </div>
        </div>
    </div>
{/if}