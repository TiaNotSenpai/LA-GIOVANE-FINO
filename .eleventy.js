module.exports = function(eleventyConfig) {
  // Imposta le cartelle di input e output
  // Leggiamo da /src e scriviamo il sito finito in /_site
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/admin"); // Copiamo anche la futura cartella admin

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes" // Le diciamo dove trovare i layout
    }
  };
};