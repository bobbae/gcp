
class NavBar extends React.Component{
  state = {
    content:[
      { id:1, description:"<iframe src='https://docs.google.com/presentation/d/e/2PACX-1vSkY_Kv5cqjWVPrnH8KQ71q_D4ZJqbAWZf-ehSOjQxu3FxL0H4ugz0Sj89pXQIYTiuCsjTcYAuXOMRU/embed?start=false&loop=false&delayms=60000' frameborder='0' width='960' height='569' allowfullscreen='true' mozallowfullscreen='true' webkitallowfullscreen='true'></iframe>"},
      { id:2, description:"<iframe src='https://sadasystems.looker.com/embed/public/Bfb9hHS8j7YRJGVjnpgB4TQPJPWNTYkr' width='600' height='338' frameborder='0'></iframe>" },
      { id:3, description:"<iframe src='https://sadasystems.looker.com/embed/public/HyCtPJ7FTdbdmbGcGSccgjswRMMkwnKy' width='600' height='338' frameborder='0'></iframe>" },
      { id:4, description:"<iframe src='https://sadasystems.looker.com/embed/public/MZwB8xzp8tNMYHPJk3tP44BfZgRtTv9v' width='600' height='338' frameborder='0'></iframe>" }, 
      {id:5, description: "<iframe src='https://sadasystems.looker.com/embed/public/2jZfvbMmXVCC6P4chGBSZQNJVgyZd3fb' width='600' height='338' frameborder='0'></iframe>"}
    ],
    listItems: [
      { id:1, name:'Home', active: false },
      { id:2, name:'Workforce', active: false },
      { id:3, name:'Gender', active: false},
      { id:4, name:'Racial Representation', active: false },
      { id:5, name:'Leadership Representation', active: false }
    ],
    body:null,
  }

  componentDidMount(){
    this.showContentHandler(1);
  }

  showContentHandler = (id) =>{
    const body={...this.state.body}
    this.state.content.map((item)=>{
      if(item.id == id){
        this.setState({body:item.description});
      }
    });
    
    const listItems = [...this.state.listItems];
    for(let item of listItems){
       item.active = false;
    }
     
    const listIndex = this.state.listItems.findIndex(item=>{
       return item.id===id;
    });
    const listItem = {
      ...this.state.listItems[listIndex]
    }
    listItem.active = true;
    listItems[listIndex] = listItem;
    this.setState({listItems:listItems});
  }

  showSideDrawer = (elename)=>{
    let element = document.getElementById(elename);
    element.className ==='NavList' ? element.className+=' responsive' : element.className = 'NavList';
  }
  
  render(){
    return(
      <div>
        <div className="NavList" id="NavBar">
          {this.state.listItems.map(item=>{
            return(
              <a onClick={()=>this.showContentHandler(item.id)} key={item.id} href="#"className={item.active? 'active' : ''}>{item.name}</a>)
          })}
          <a className="icon" onClick={()=>this.showSideDrawer("NavBar")} href="#"><i className="fa fa-bars"></i></a>
      </div>
        <div className="contentDivClass"  dangerouslySetInnerHTML={{ __html: this.state.body }}>
        </div>
      </div>
    );
  }
}


class App extends React.Component{
  render(){
    return(
      <div>
        <NavBar/>
      </div>
    );
  }
}

ReactDOM.render(<App/>, document.getElementById('root'));