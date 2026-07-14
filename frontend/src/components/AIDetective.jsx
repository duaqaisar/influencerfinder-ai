import {motion} from "framer-motion";
import "../styles/detective.css";


export default function AIDetective(){

return (

<motion.div
className="detective"
animate={{
y:[0,-20,0]
}}
transition={{
duration:3,
repeat:Infinity
}}
>

<div className="head">

<div className="eye left"></div>
<div className="eye right"></div>

</div>


<div className="body">

</div>


<div className="scan">

</div>


</motion.div>

)

}
