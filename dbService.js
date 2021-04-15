const mysql = require('mysql');
const dotenv = require('dotenv');
let instance = null;
dotenv.config();

// const connection = mysql.createConnection({
//     host: 'bemvgo8nokzzatzk1jik-mysql.services.clever-cloud.com',
//     user: 'u2jnj1s64todnegn',
//     password: 'oF2UhdcDwSfqp6dIxbmC',
//     database: 'bemvgo8nokzzatzk1jik'
// });

// connection.connect((err) => {
//     if (err) {
//         console.log(err.message);
//     }
//     console.log('db ' + connection.state);
// });

var db_config = {
    host: 'b8rcs00irv3k6mphmfte-mysql.services.clever-cloud.com',
    user: 'utbp135gid0b691w',
    password: 'RaoG02eY2Ktc5tdyEViY',
    database: 'b8rcs00irv3k6mphmfte'
  };
  
  var connection;
  
  function handleDisconnect() {
    connection = mysql.createConnection(db_config); // Recreate the connection, since
                                                    // the old one cannot be reused.
  
    connection.connect(function(err) {              // The server is either down
      if(err) {                                     // or restarting (takes a while sometimes).
        console.log('error when connecting to db:', err);
        setTimeout(handleDisconnect, 2000); // We introduce a delay before attempting to reconnect,
      }  
      else
      {
          console.log('Connected');
      }                                   // to avoid a hot loop, and to allow our node script to
    });                                     // process asynchronous requests in the meantime.
                                            // If you're also serving http, display a 503 error.
    connection.on('error', function(err) {
      console.log('db error', err);
      if(err.code === 'PROTOCOL_CONNECTION_LOST') { // Connection to the MySQL server is usually
        handleDisconnect();                         // lost due to either server restart, or a
      } else { 
        handleDisconnect();   
                                              // connnection idle timeout (the wait_timeout
        // throw err;                                  // server variable configures this)
      }
    });
  }
  
  handleDisconnect();

  async function  checkUser(email,isDev){
    try{
      var query;
      const user = await new Promise((resolve, reject) => {
        if(isDev)
         query = "SELECT * FROM developer WHERE email = ? ";
        else
        query = "SELECT * FROM tester where email =? ";

        connection.query(query, [email] , (err, result) => {
            if (err) reject(new Error(err.message));
            resolve(result);
        })
    });
      console.log(user);
      if(user.length==0)
      return false;
      else
      return true;
      //return user;
    }
    catch{return false;}
  }
  
class DbService {

    static getDbServiceInstance() {
        return instance ? instance : new DbService();
    }
    async getUserById(id,isDev){
      try{
        var query;
        
        const user = await new Promise((resolve,reject)=>{
        if(isDev)
         query = "SELECT * FROM developer WHERE id=?";
        else
         query = "SELECT * FROM tester WHERE id=?";
        connection.query(query,[id],(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          })
        });
        if(user.length == 0){
          return {
            userFound:false,
            error:false
          };
        }
        return {
          userFound:true,
          name:user[0].name,
          email:user[0].email,
          error:false
        }

      }
      catch{
        return{
          error:true
        };
      }
    }
  
    async registerUser(name,email,password,isDev){
      try{
        const db=DbService.getDbServiceInstance();
        var userExists=await checkUser(email,isDev);
        var query;
        if(userExists){
          return {
            name:name,
            register: "already registered",
            error:false
          };}
        console.log(userExists);
        
        
        const user = await new Promise((resolve,reject)=>{
          if(isDev)
          query = "INSERT INTO developer (name,email,password) VALUES (?,?,?)";
          else
          query = "INSERT INTO tester (name,email,password) VALUES (?,?,?)";
        connection.query(query,[name,email,password],(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          })
        });
        console.log(user);
        return{
          name:name,
          registered:true,
          error:false

        };
      }
      catch{
        return {
          error:true
      };
      }
    }
    async getUser(id){
      try{
        const user = await new Promise((resolve, reject) => {
          const query = "SELECT * FROM users WHERE email = ? AND password=?";
          connection.query(query, [email,password] , (err, result) => {
              if (err) reject(new Error(err.message));
              resolve(result);
          })
      });
      if(user.length==0)
      {
          return {
              userFound : false,
              error:false

          };
      }
      return {
          userFound : true,
          username : user[0].username,
         // password : user[0].password,
          id : user[0].id,
          error:false
      };

      }
      catch (error) {
              return {
                  error:error.message
              };
          }
    }
async changeBugStatus(id){
  try{
    const bug = await new Promise((resolve,reject)=>{
      const query = 'UPDATE bug SET status = "testing" where id=?';
      connection.query(query,[id], (err, result) => {
        if (err) reject(new Error(err.message));
        resolve(result);
    })
    })
    return{
      updated:true,
      error:false
    };
    }
  catch(err){
    return {error:err.message}
  }
} 
async getOpenBugs(){
      try{
        
        const bugs = await new Promise((resolve,reject)=>{
          const query = 'SELECT * FROM bug where assignedTo= 0 ORDER BY severity DESC';
          connection.query(query, (err, result) => {
            if (err) reject(new Error(err.message));
            resolve(result);
        })
    });
      if(bugs.length==0)
      {
          return {
              bugFound : false,
              error:false

          };
      }
      return{
        bugFound:bugs,
        error:false
      }
        
      }
      catch(err){
        return {error:err.message}
      }
    }
    async authUser(email,password,isDev) {
      //console.log(email,password);
          try {
            var query;
              const user = await new Promise((resolve, reject) => {
                if(isDev)
                query="SELECT * FROM developer WHERE email = ? AND password=?;"
                else
                query="SELECT * FROM tester WHERE email = ? AND password=?;"
                  connection.query(query, [email,password] , (err, result) => {
                      if (err) reject(new Error(err.message));
                      resolve(result);
                  })
              });
              if(user.length==0)
              {
                  return {
                      userFound : false,
                      error:false

                  };
              }
              //console.log(user[0].name,user[0].email,user[0].activeIssues,user[0].createdIssues,user[0].solvedIssues);
              if(isDev){
                return{
                  userFound:true,
                  id:user[0].id,
                  username:user[0].name,
                  email:user[0].email,
                  activeIssues:user[0].activeIssues,
                  createdIssues:user[0].createdIssues,
                  solvedIssues:user[0].solvedIssues,

                };
              }
              return {
                  userFound : true,
                  username : user[0].username,
                  email:user[0].email,
                  testedIssues:user[0].testedIssues,
                  createdIssues:user[0].createdIssues,
                  error:false
              };
          } 
          catch (error) {
              return {
                  error:true
              };
          }
    }
    async getStatusBugs(status){
      console.log(status);
      try{
        const bugs = await new Promise((resolve,reject)=>{
          const query = 'SELECT * FROM bug where status= ?;';
          connection.query(query,[status],(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          });
        });
        console.log(bugs);
        if(bugs.length==0){
          return{
            bugFound:false,
            
            error:false
          };
        }

        return{
          bugFound:true,
          details:bugs,
          error:false
        }
      }
      catch{
        return{
          error:true
        };

      }
    }
    async getSeverityBugs(severity){
      console.log(severity);
      try{
        const bugs = await new Promise((resolve,reject)=>{
          const query = 'SELECT * FROM bug where severity= ?;';
          connection.query(query,[severity],(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          });
        });
        console.log(bugs);
        if(bugs.length==0){
          return{
            bugFound:false,
            
            error:false
          };
        }

        return{
          bugFound:true,
          details:bugs,
          error:false
        }
      }
      catch{
        return{
          error:true
        };

      }
    }
    async getBugDetails(bugId){
      try{
        const bug =await new Promise ((resolve,reject)=>{
          const query = 'SELECT * FROM bug where id =?;';
          connection.query(query,[bugId],(err,result)=>{
            if(err) reject(new Error (err.message));
            resolve(result);
          });
        })
        if(bug.length==0){
          return {
            bugFound:false,
            error:false
          }
        }
        return {bug:bug};
      }
      catch(err){
        return {
          error:err.message
        }
      }
    }
    async createBug(name,createdAt,status,severity,description,createdBy,assignedTo,testedBy,sprintId){
      try{
        const set = await new Promise((resolve,reject)=>{
          const query = 'INSERT INTO bug (name,createdAt,status,severity,description,createdBy,assignedTo,testedBy,sprintId) VALUES(?,?,?,?,?,?,?,?,?);'
          connection.query(query,[name,createdAt,status,severity,description,createdBy,assignedTo,testedBy,sprintId],(err,result)=>{
            if(err) reject(new Error (err.message));
            resolve(result);
          });
        })
      
      return{
        added:true,
        error:false
      }
    }
      catch(err){
        return{
          error:err.message
        }
      }
    }
    async sendToTesting(bugId,devId){
      try{
        const set = await new Promise((resolve,reject)=>{
        const query1 = 'UPDATE bug SET  status ="testing" WHERE id=?;';
        const query2 = 'UPDATE developer SET activeIssues=activeIssues-1 where id=?;';
        connection.query(query1,[bugId],(err,result)=>{
          if(err) reject(new Error (err.message));
          resolve(result);
        });
        connection.query(query2,[devId],(err,result)=>{
          if(err) reject(new Error (err.message));
          resolve(result);
        })
        })
        return {
          updated:true,
          
        }
      }
      catch(err){
        return {
          updated:true,
        }
      }
    }
    async assignBug(bugId,devId){
      try{
        const set = await new Promise((resolve,reject)=>{
        const query1 = 'UPDATE bug SET assignedTo=? , status ="active" WHERE id=?;';
        const query2 = 'UPDATE developer SET activeIssues=activeIssues+1 where id=?;';
        connection.query(query1,[devId,bugId],(err,result)=>{
          if(err) reject(new Error (err.message));
          resolve(result);
        });
        connection.query(query2,[devId],(err,result)=>{
          if(err) reject(new Error (err.message));
          resolve(result);
        })

        })
        return {
          updated:true,
          error:false
        }
      }
      catch(err){
        return {
          error:err.message
        }
      }
    }
    async getBugsById(id,isDev){
      try{
        const bug = await new Promise((resolve,reject)=>{
          var query;
          if(isDev)
          query='SELECT * FROM bug WHERE assignedTo=? ORDER BY severity DESC';
          else
          query='SELECT * FROM bug WHERE testedBy=? ORDER BY severity DESC';
          connection.query(query,[id],(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          });

        });
        console.log(bug);
        if(bug.length==0)
        return{
          bugFound:false,
          error:false
        }
        var bugs=[];//send id ,name,severity only
       for(var i=0;i<bug.length;i++){
         var ar=[];
         bugs.push(bug[i]);
       }
       return bugs;
      }
      catch{
        return{
          error:true
        };

      }
    }
    async getBugs(){
      try{
        const bug = await new Promise((resolve,reject)=>{
          const query = 'SELECT id,name,severity FROM bug ORDER  BY createdAt DESC LIMIT 10;';
          connection.query(query,(err,result)=>{
            if(err) reject(new Error(err.message));
            resolve(result);
          });
        });
        console.log(bug);
        if(bug.length==0)
        return{
          bugFound:false,
          
          error:false
        };
       var bugs=[];
       for(var i=0;i<bug.length;i++){
         bugs.push(bug[i]);
       }
       return bugs;
      }
      catch{
        return{
          error:true
        };

      }
    }


  };

    
module.exports = DbService;

