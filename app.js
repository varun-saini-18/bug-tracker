const express = require('express');
const app = express();
const dbService = require('./dbService');
//const passport = require("passport");
const session = require("express-session");
//const flash = require("express-flash");
const bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
app.use(
  session({
    // Key we want to keep secret which will encrypt all of our information
    secret: 'Cat',
    // Should we resave our session variables if nothing has changes which we dont
    resave: false,
    // Save empty value if there is no vaue which we do not want to do
    saveUninitialized: false
  })
);

app.use(express.json());
//app.set("view engine", "ejs");
//app.use(express.static(__dirname + '/views'));
app.get('/getopenbugs',(req,res)=>{
  const db = dbService.getDbServiceInstance();
  const result = db.getOpenBugs();
  result.then(data => {
          res.json({data : data})
      })
  .catch(err => console.log(err));
})

app.post('/user/login',(request,response) => {
    const db = dbService.getDbServiceInstance();
    console.log(request.body);
    const {email,password,isDev}= request.body;
    console.log(email,password);
    const result = db.authUser(email,password,isDev);
    result.then(data => {
            response.json({data : data})
        })
    .catch(err => console.log(err));
  })

app.get('/getuser',(req,res)=>{
  const db = dbService.getDbServiceInstance();
  const {id,isDev}=req.body;
  const result = db.getUserById(id,isDev);
  result.then(data=>{
    res.json({data:data})
  })
  .catch(err=>{
    res.json({error:err.message});
  })
})
app.post('/register',(req,res)=>{
  const db=dbService.getDbServiceInstance();
  const {name,email,password,isDev}=req.body;
  const result = db.registerUser(name,email,password,isDev);
  result.then(data=>{
    res.json({data:data})
  })
  .catch(err=> {
    res.json({error:err.message})
  })
});
app.post('/assignbug',(req,res)=>{
  const db=dbService.getDbServiceInstance();
  const {bugId,devId}=req.body;
  const result=db.assignBug(bugId,devId);
  result.then(data=>{
    res.json({data:data})
  })
  .catch(err=>{
    return {error:true}
  })
})
app.post('/sendtotesting',(req,res)=>{
  const db=dbService.getDbServiceInstance();
  const {bugId,devId}=req.body;
  const result=db.sendToTesting(bugId,devId);
  result.then(data=>{
    res.json({data:data})
  })
  .catch(err=>{
    return {error:true}
  })
})
app.post('/changebugstatus',(req,res)=>{
  const db=dbService.getDbServiceInstance();
  const {id}=req.body;
  const result=db.changeBugStatus(id);
  result.then(data=>{
    res.json({data:data})
  })
  .catch(err=>{
    return{error:true};
  })
})
  app.get('/getbugs',(req,res)=>{
    const db=dbService.getDbServiceInstance();
    const result=db.getBugs();
    console.log(result);
    result.then(data=>{
      res.json({data:data})
    })
    .catch(err=>{
      return {error:true};

    })
  });
  app.post('/getbugdetail',(req,res)=>{
    const db=dbService.getDbServiceInstance();
    const {bugId}=req.body;
    const result=db.getBugDetails(bugId);
    console.log(result);
    result.then(data=>{
      res.json({data:data})
    })
    .catch(err=>{
      return {error:true};
    })

  })
  app.post('/createbug',(req,res)=>{
    const db=dbService.getDbServiceInstance();
    const {name,createdAt,status,severity,description,createdBy,assignedTo,testedBy,sprintId}=req.body;
    const result=db.createBug(name,createdAt,status,severity,description,createdBy,assignedTo,testedBy,sprintId);
    console.log(result);
    result.then(data=>{
      res.json({data:data})
    })
    .catch(err=>{
      return {error:true};
    })

  })
  app.post('/getbugsbyid',(req,res)=>{
    const db=dbService.getDbServiceInstance();
    const {id,isDev}=req.body;
    console.log(id,isDev); 
    const result=db.getBugsById(id,isDev);
    console.log(result);
    result.then(data=>{
      res.json({data:data})
    })
    .catch(err=>{
      return {error:true};
    })
    
  })
app.get("/", (req, res) => {
  res.json({name : "Kashika"})
});

const port = process.env.PORT || '5000';
app.listen(port, () => console.log(`Server started on Port ${port}`));