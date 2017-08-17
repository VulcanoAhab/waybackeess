import scala.util.matching.Regex
import scala.io.Source


class snapProcessor {
  //base vars
  var _raw="notSet";
  var _onlyText=None;
  //processors
  val rex="(?<=href=\").*?\"".r;
  val cleanUrl="(?:http://web.archive.org)?/web/\\d+(?:im_)?/".r;

  //workers
  def loadText(_snapFile:String){
    var _fd=Source.fromFile(_snapFile);
     _raw=_fd.mkString;
    _fd.close
    println("[+] Loaded text | Length: %d".format(_raw.length()))
  }

  def grabUrls(){
    val rawUrls=rex.findAllIn(_raw);

    if (rawUrls.hasNext) {
      val targetUrls=rawUrls.filter(!_.startsWith("/static/"));
      var goodUrls=targetUrls.map(x => cleanUrl.replaceAllIn(x,""));
      val _urls=goodUrls.toList;
      print("[+] Mined %d urls".format(_urls.length()))
    }
  }

}






// object parseSnap {
//
//   var _text="TestText"
//
//   def main (args:Array[String]){
//     /* snap parser
//        scala versios
//     */
//     var snapis= new snapProcessor()
//     snapis.loadText("testSnapHtml.txt")
//     snapis.grabUrls()
//   }
//
// }
