<script lang="ts">
    export let data;
    import NavBar from "$lib/NavBar.svelte";
    const username = data.username;
</script>

<header>
    <NavBar { username }/>
</header>
<main class="p-16 pt-28 overflow-auto tall:overflow-hidden">
    <slot />
</main>