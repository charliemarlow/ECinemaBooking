package ecinema;
import java.security.SecureRandom;
import java.security.MessageDigest;
import java.lang.Object;


abstract class User{

    protected String userID;
    private String password;

		public String getUserID(){
        return userID;
		}

    public void setUserID(String ID){
        userID = ID;
		}


    public String getPassword(){
        return password;
		}

    public void setPassword(String passwd){
        password = passwd;
		}

    public String hashPassword(String pass)
    {
	/*
	SecureRandom random = new SecureRandom();
	byte[] salt = new byte[16];
	random.nextBytes(salt);
	MessageDigest md = MessageDigest.getInstance("SHA-512");
	md.update(salt);
	byte[] hashedPassword = md.digest(passwordToHash.getBytes(StandardCharsets.UTF_8));
	*/
	String pw_hash = BCrypt.hashpw(pass, BCrypt.gensalt());
	System.out.println(pw_hash);
    }//hashPassword

}


