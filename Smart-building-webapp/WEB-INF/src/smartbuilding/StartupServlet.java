package smartbuilding;
 
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.FileHandler;
import java.util.logging.SimpleFormatter;


 
public class StartupServlet extends HttpServlet {
   
   private static final Logger LOGGER = Logger.getLogger("StartupServlet-Logger");
      FileHandler fh;  

      int count = 0;

      public void init() throws ServletException
      {
         try {  
            // This block configure the logger with handler and formatter  
            fh = new FileHandler("StartupServlet-LogFile.log");  
            LOGGER.addHandler(fh);
            SimpleFormatter formatter = new SimpleFormatter();  
            fh.setFormatter(formatter);  

         }catch (SecurityException e) {  
            e.printStackTrace();  
         }catch (IOException e) {  
            e.printStackTrace();  
         } 


        MyRunnableImplementation r = new MyRunnableImplementation();

        // Create a new Thread instance, provide the task that we want to run
        // (by providing the Runnable as an argument) and give the thread a name.
        // Now we can use Thread.start() to run it!
        Thread thread1 = new Thread(r, "Thread 1");
        thread1.start();

         LOGGER.info("Logger Name: "+LOGGER.getName());
         
            LOGGER.warning("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + count + "!!!!!!!!!!!!!!!!!!!!");
      
          System.out.println("----------");
          System.out.println("---------- Testing ----------");
          System.out.println(count);
          System.out.println("----------");
          count ++;
          
          try{
            Thread.sleep(5000);
          }catch(InterruptedException e){
            System.out.println(e);
          }   
         
           
      }

}

