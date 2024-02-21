import mongoose from 'mongoose';

const reviewSchema = new mongoose.Schema({
  // title: {
  //   type: String,
  //  
  // },
  rating: {
    type: String,
  
  },
  star: {
    type: Number,
  
  },
  body: {
    type: String,
  
  },
  fullDate: {
    type: String,
  
  },
  date: {
    type: String,
  
  },
})

const sentimentSchema = new mongoose.Schema({
  negative: {
    type: Number,
  
  },
  neutral: {
    type: Number,
  
  },
  positive: {
    type: Number,
  
  },
})

const keywordSchema = new mongoose.Schema({
  word: {
    type: String,
  
  },
  score: {
    type: Number,
  
  },
})

const svaSchema = new mongoose.Schema({
  date: {
    type: String,
  
  },
  score: {
    type: Number,
  
  },
})

const aspecSentimentSchema = new mongoose.Schema({
  aspect: {
    type: String,
  
  },
  label: {
    type: String,
  
  },
  score: {
    type: Number,
  
  },
})

const productSchema = new mongoose.Schema({
  name: {
    type: String,
  
  },
  url: {
    type: String,
  
  },
  price: {
    type: String,
  
  },
  image: {
    type: String,
  
  },
  description: {
    type: String,
  
  },
  date: {
    type: String,
  
  },
  avgRating: {
    type: String,
  
  },
  reviews: [reviewSchema],
  sentiment: sentimentSchema,
  keywords: [keywordSchema],
  aspecSentiment: [aspecSentimentSchema],
  sva: [svaSchema],
  topicModel: {
    type: Object,
  
  }
});

const userSchema = new mongoose.Schema({
  name: {
    type: String,
  
  },
  email: {
    type: String,
  
    unique:true,
  },
  phone: {
    type: Number,
    required: false,
  },
  password: {
    type: String,
  
  },
  products: [productSchema]
});

const User = mongoose.model("cres_user", userSchema);

export default User;