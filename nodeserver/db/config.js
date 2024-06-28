import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

const DB =
  "mongodb+srv://sonarsiddhesh105:K5NuO27RwuV2R986@cluster0.0aedb3y.mongodb.net/?retryWrites=true&w=majority";

function init() {
  if (!DB) console.log("DB not found in env");
  mongoose
    .connect(DB, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    })
    .then(() => {
      console.log(`DB connected`);
    })
    .catch((err) => console.log(`DB connection failed ${err}`));
}

export default init;
