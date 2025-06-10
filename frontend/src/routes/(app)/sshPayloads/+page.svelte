<svelte:head>
    <title>SSH - Shorklights</title>
</svelte:head>

<script lang="ts">
    import { enhance } from '$app/forms';
    import { onMount } from 'svelte';

    let requestWaiting = false;
    let alreadyRequested = false;
    let showModalPayloads = false;
    let payloadsType = '';
    let payloadsWindow = 'upload';
    let file: File | null = null;
    let imageUrl: string | null = null;
    let fileName: string = '';

    let modalServer: HTMLElement | null = null;
    let serversList: HTMLElement | null = null;

    onMount(() =>{
        modalServer = document.getElementById('modalServer')
        serversList = document.getElementById('server-list')
    })

    function openServerList() {
        if (modalServer) { modalServer.classList.remove('hidden'); modalServer.classList.add('flex');}
        if (alreadyRequested) return;
        requestWaiting = true;

        return ({ result }: { result: { data: { servers: any[] } } }) => {
            try {
                if (serversList) {
                    serversList.innerHTML = '';
                    if (result.data.servers && Array.isArray(result.data.servers)) {
                        result.data.servers.forEach(server => {
                            const onlineClass = server.status === "online" ? "text-sky-400" : "text-gray-400";
                            const onlineStatus = server.status === "online" ? '✿ Online' : '✿ Offline';

                            serversList.innerHTML += `
                            <label class="server-item flex items-center cursor-pointer w-full p-2 rounded-md bg-gray-800 hover:bg-gray-700" data-id="${server._id}">
                                <input type="checkbox" class="mr-2 hidden" />
                                <span class="${onlineClass}">${onlineStatus}</span><span class="mx-2">|</span> ${server.name} (${server.ip})
                            </label>`
                        });

                        serversList.querySelectorAll(".server-item").forEach(item => {
                            item.addEventListener('click', (e) => {
                                const checkbox = item.querySelector('input[type="checkbox"]') as HTMLInputElement | null;
                                if (checkbox) {
                                    checkbox.checked = !checkbox.checked;
                                    item.className = `server-item flex items-center cursor-pointer w-full p-2 rounded-md ${
                                        checkbox.checked ? 'bg-sky-800 hover:bg-sky-700' : 'bg-gray-800 hover:bg-gray-700'
                                    }`;
                                }
                            });
                        })
                    } else {
                        serversList.innerHTML = '<p class="text-gray-300">No servers found.</p>';
                    }
                }
            } catch (error) {
                console.error('Error refreshing server list:', error);
            } finally {
                requestWaiting = false;
                alreadyRequested = true;
            }
        }
    }

    function closeServerList() {
        if (modalServer) { modalServer.classList.add('hidden'); modalServer.classList.remove('flex'); getSelectedServers()}
    }

    function getSelectedServers() {
        const serverList = document.querySelectorAll('.server-item');
        const selectedServers: string[] = [];
        serverList.forEach(item => {
            try {
                const checkbox = item.querySelector('input[type="checkbox"]') as HTMLInputElement | null;
                if (checkbox.checked) {
                    const serverId = item.getAttribute('data-id');
                    selectedServers.push(serverId);
                }
            } catch (e) {
                console.error("Oops")
            }
        });
        return selectedServers;
    }

    function handleFileChange(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            file = target.files[0];
            if (file && file.type.startsWith('image/') && payloadsType === 'changeWallpaper' || (file.type === 'audio/mpeg' && payloadsType === 'playSounds')) {
                imageUrl = URL.createObjectURL(file);
                fileName = file.name;
            } else {
                imageUrl = null;
            }
        }
    }

    function handleDrop(event: DragEvent) {
        event.preventDefault();
        const input = document.getElementById('fileInput') as HTMLInputElement | null;
        if (event.dataTransfer && event.dataTransfer.files.length > 0 && input) {
            const droppedFile = event.dataTransfer.files[0];
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(droppedFile);
            input.files = dataTransfer.files;

            file = droppedFile;
            if (
                (file.type.startsWith('image/') && payloadsType === 'changeWallpaper') ||
                (file.type === 'audio/mpeg' && payloadsType === 'playSounds')
            ) {
                imageUrl = URL.createObjectURL(file);
                fileName = file.name;
            } else {
                imageUrl = null;
            }
        }
    }

    function handleUpload() {
        const selectedServers = getSelectedServers();
        const form = document.getElementById('payloadForm') as HTMLFormElement | null;
        if (!form) return;

        // Remove old hidden server inputs
        form.querySelectorAll('input[name="servers"]').forEach(e => e.remove());

        // Add hidden inputs for each selected server
        selectedServers.forEach(serverId => {
            if (serverId) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'servers';
                input.value = serverId;
                form.appendChild(input);
            }
        });

        form.requestSubmit();
    }
</script>

<section id="header" class="relative flex flex-col items-center z-20">
    <h1 class="text-4xl md:text-5xl font-bold text-center">
        <span class="text-sky-400">S</span>S<span class="text-sky-400">H</span>
    </h1>
    <div class="mt-1">
        <form method="POST" action="?/getServers" use:enhance={openServerList}>
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
            <button type="button" on:click={() => {payloadsType = 'changeWallpaper'; showModalPayloads= true}} class="flex flex-col items-center justify-center w-full max-w-xs md:w-72 m-2 h-56 bg-gray-900 rounded-lg border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 cursor-pointer hover:bg-gray-800 transition duration-200">
                <i class="icon-[iconamoon--folder-image] text-6xl text-sky-400 drop-shadow"></i>
                <p class="font-semibold text-lg text-center">Change wallpaper</p>
            </button>
            <button type="button" on:click={() => {payloadsType = 'playSounds'; showModalPayloads= true}} class="flex flex-col items-center justify-center w-full max-w-xs md:w-72 m-2 h-56 bg-gray-900 rounded-lg border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 cursor-pointer hover:bg-gray-800 transition duration-200">
                <i class="icon-[iconamoon--music-2] text-6xl text-sky-400 drop-shadow"></i>
                <p class="font-semibold text-lg text-center">Play sounds</p>
            </button>
        </article>
    </section>
</section>

<div id='modalServer' class="fixed inset-0 bg-black/70 items-center justify-center hidden z-50">
    <div class="bg-gray-900 p-8 rounded-2xl border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 max-w-md w-full relative">
        <div class="flex items-center gap-4 mb-4">
            <input class="w-full border border-gray-700 bg-gray-800 text-white p-2 rounded-md" placeholder="Search servers..."/>
            <button class="text-sky-400 text-3xl font-bold hover:text-red-500 transition cursor-pointer duration-200" aria-label="Close" on:click={() => closeServerList()}>&times;</button>
        </div>
        <div id="server-list" class="flex flex-col items-center justify-center gap-2 min-h-2">
            {#if requestWaiting}
                <div class="loader"></div>
            {/if}
        </div>
    </div>
</div>

{#if showModalPayloads}
    <div class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="bg-gray-900 p-8 m-8 max-w-3xl w-full min-h-94 max-h-[42vh] h-full rounded-2xl border border-sky-400/90 shadow-[0_0_40px_3px] shadow-sky-400/60 relative flex flex-col">
            <form id="payloadForm" method="POST" class="flex flex-col h-full" action="?/executePayload" enctype="multipart/form-data" use:enhance>
                <div class="flex items-center justify-between gap-4 mb-6">
                    <div class="flex flex-col md:flex-row md:items-center">
                        {#if payloadsType === 'changeWallpaper'}
                            <h2 class="text-xl font-bold text-white">Change Wallpaper</h2>
                        {:else if payloadsType === 'playSounds'}
                            <h2 class="text-xl font-bold text-white">Play Sounds</h2>
                        {/if}
                        <span class="mx-2 text-gray-500 select-none hidden md:flex">|</span>
                        <div class="flex items-center gap-2 mt-2 md:mt-0">
                            <button class="bg-gray-700 p-1 rounded-md hover:text-sky-300 transition duration-200 cursor-pointer" class:text-sky-400={payloadsWindow === 'upload'} on:click={() => payloadsWindow = 'upload'}>Upload</button>
                                <button class="bg-gray-700 p-1 rounded-md hover:text-sky-300 transition duration-200 cursor-pointer" class:text-sky-400={payloadsWindow === 'library'} on:click={() => payloadsWindow = 'library'}>Library</button>
                        </div>
                    </div>
                    <button class="text-sky-400 text-3xl font-bold hover:text-red-500 transition cursor-pointer duration-200" aria-label="Close" on:click={() => { showModalPayloads = false; imageUrl=null; fileName="" }}>&times;</button>
                </div>
                {#if payloadsWindow === 'upload'}
                    <button type="button" on:drop={handleDrop} on:dragover|preventDefault on:click={() => document.getElementById('fileInput')?.click()} class="w-full h-full bg-gray-800 flex flex-col items-center justify-center border-1 border-dashed border-sky-400 rounded-lg transition hover:border-sky-300 hover:bg-gray-700 cursor-pointer">
                        {#if imageUrl}
                            {#if payloadsType === 'changeWallpaper'}
                                <img src={imageUrl} alt="Preview" class="mt-2 mb-2 max-h-40 rounded shadow" />
                                {:else if payloadsType === 'playSounds'}
                                <i class="icon-[iconamoon--music-2] text-5xl text-sky-400 mb-3"></i>
                            {/if}
                        {:else}
                            <i class="icon-[iconamoon--cloud-upload] text-5xl text-sky-400 mb-3"></i>
                        {/if}
                        <span class="text-white text-md md:text-lg font-medium">{fileName || 'Drop files here or click to upload'}</span>
                            <input id="fileInput" name="file" type="file" class="hidden" on:change={handleFileChange} accept={payloadsType === 'changeWallpaper' ? '.png,.jpg,.jpeg' : '.mp3'}/>
                        {#if !imageUrl}
                            {#if payloadsType === 'changeWallpaper'}
                                <span class="text-gray-400 text-sm mt-2">Supported: PNG, JPG, JPEG</span>
                            {:else if payloadsType === 'playSounds'}
                                <span class="text-gray-400 text-sm mt-2">Supported: MP3</span>
                            {/if}
                        {/if}
                    </button>
                    {:else if payloadsWindow === 'library'}
                    <div class="flex flex-col items-center justify-center h-full">
                        <p class="text-gray-400">Library is not implemented yet.</p>
                    </div>
                {/if}
                <div class="flex justify-center items-center">
                    <input type="hidden" name="payloadType" value={payloadsType} />
                    <button on:click={() => handleUpload()} type="button" class="mt-2 px-4 py-2 bg-sky-400 w-auto text-white font-semibold rounded-lg shadow hover:bg-red-500 cursor-pointer self-center transition duration-200 flex items-center gap-2">
                        Execute
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}