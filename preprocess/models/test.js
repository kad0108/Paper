function ListNode(x){
    this.val = x;
    this.next = null;
}
function FindKthToTail(head, k)
{
    var len = getLen(head);
    if(!k || len < k) return {};
    var p = head;
    for(var i = 1; i <= len-k; i++){
        p = p.next;
    }
    return p;
    
    function getLen(head){
        var len = 0;
        var p = head;
        while(p){
            p = p.next;
            len++;
        }
        return len;
    }
}

var head = new ListNode(1);
var p = head;
for(var i = 2; i <= 8; i++){
	p.next = new ListNode(i);
	p = p.next;
}
console.log(FindKthToTail(null, 8));
// console.log(FindKthToTail(head, 1).val);

