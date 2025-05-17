<script lang="ts">
	import '../app.css';
    import NavBar from "$lib/NavBar.svelte";
    import { onNavigate} from "$app/navigation";

    onNavigate(() => {
        if (!document.startViewTransition) {
            return;
        }

        return new Promise<void>((resolve) => {
            document.startViewTransition(() => {
                resolve();
            });
        });
    });
</script>

<header>
    <NavBar />
</header>
<main class="p-16 pt-28 overflow-auto lg:overflow-hidden">
    <slot />
</main>
