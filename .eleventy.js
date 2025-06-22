module.exports = function(eleventyConfig) {
  
  // La funzione "Passthrough" è il modo più robusto per copiare
  // i nostri asset (CSS, JS, Immagini) nella cartella finale del sito.
  eleventyConfig.addPassthroughCopy("./src/css/");
  eleventyConfig.addPassthroughCopy("./src/js/");
  eleventyConfig.addPassthroughCopy("./src/images/");

  // Aggiungiamo la futura cartella per il CMS
  eleventyConfig.addPassthroughCopy("./src/admin/");
  
  // Questa è la configurazione più esplicita possibile delle directory.
  return {
    // Specifichiamo che i template che Eleventy deve processare sono questi:
    templateFormats: ["md", "njk", "html"],
    
    // Specifichiamo che sia i file Markdown che HTML devono usare
    // il motore di template Nunjucks (che ci permette di usare {{ variabili }}).
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",

    dir: {
      input: "src",          // La nostra cartella sorgente
      includes: "_includes", // La sottocartella per i layout
      data: "_data",         // Per dati futuri
      output: "_site"        // La cartella dove viene costruito il sito finale
    }
  };
};