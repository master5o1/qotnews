<script>
  import Time from "../components/Time.svelte";
  export let story;
</script>

<Time date={story.date} />
{#if story.author && story.author_link}
  by
  <a class="author" href={story.author_link}>{story.author}</a>
{:else if story.author}by <span class="author">{story.author}</span>{/if}
on
<a class="source" href={story.link || story.url}>{story.source}</a>
{#if story.score}&bull; {story.score} points{/if}
{#if Number(story.num_comments)}
  &bull;
  <a rel="prefetch" href="/{story.id}#comments">{story.num_comments}
    comments</a>
{/if}
