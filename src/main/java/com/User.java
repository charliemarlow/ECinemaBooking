package ecinema;

abstract class User{

    private String userID;
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
}


