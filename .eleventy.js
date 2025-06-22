module.exports = function(eleventyConfig) {
  
  // LA SOLUZIONE: "LAYOUT ALIASING"
  // Diciamo a Eleventy: "Ogni volta che vedi 'layout: base',
  // usa il file che si trova in 'layouts/base.html'".
  // Questo elimina ogni possibile confusione con i percorsi.
  eleventyConfig.addLayoutAlias("base", "layouts/base.html");
  
  // Copia gli asset (CSS, JS, Immagini) nella cartella finale.
  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/js");
  eleventyConfig.addPassthroughCopy("./src/images");
  eleventyConfig.addPassthroughCopy("./src/admin");
  
  // La configurazione delle directory, corretta e confermata.
  return {
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",

    dir: {
      input: "src",
      includes: "_includes", // Cerca i layout qui dentro...
      data: "_data",
      output: "_site"
    }
  };
};