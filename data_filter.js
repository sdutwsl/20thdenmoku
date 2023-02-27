const fs = require("fs");

const catas = JSON.parse(fs.readFileSync("./books.json"));

catas.forEach((cata) => {
  cata["sub_cata"].forEach((sub_cata) => {
    sub_cata["book_list"] = sub_cata["book_list"].filter((b) => {
      if (!b["description"]) return false;
      return true;
    });
  });
});

let amount = catas.reduce((p, c) => {
  return (
    p +
    c["sub_cata"].reduce((p, c) => {
      return p + c["book_list"].length;
    }, 0)
  );
}, 0);

fs.writeFileSync("clean_books.json", JSON.stringify(catas));
console.log("books amount: " + amount);
