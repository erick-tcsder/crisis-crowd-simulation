export class Utils{
  static getPxToM(map,canvas,px){
    return px*map.width/canvas.width
  }
  static getMToPx(map,canvas,m){
    return m*canvas.width/map.width
  }
}