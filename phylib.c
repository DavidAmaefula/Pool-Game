#include <stdio.h>
#include "phylib.h" 
#include <stdlib.h>
#include <string.h>
#include <math.h>

//1st Structure
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {

phylib_object *object = malloc(sizeof(phylib_object)); 

    if (object == NULL) {

        return NULL; 

    }
object->type = PHYLIB_STILL_BALL; 
object->obj.still_ball.number = number; 
object->obj.still_ball.pos = *pos; 
return object; 
}

//2nd Structure
phylib_object *phylib_new_rolling_ball( unsigned char number, 
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc){


    phylib_object *object = malloc(sizeof(phylib_object));

    if (object == NULL){

        return NULL;

    }
    object->type = PHYLIB_ROLLING_BALL;
    object->obj.rolling_ball.number = number;
    object->obj.rolling_ball.pos = *pos;
    object->obj.rolling_ball.vel = *vel;
    object->obj.rolling_ball.acc = *acc;
    return object;
}

//3rd structure
phylib_object *phylib_new_hole( phylib_coord *pos ){

    phylib_object *object = malloc(sizeof(phylib_object));

        if (object == NULL){

            return NULL;
        }

    object->type = PHYLIB_HOLE;
    object->obj.hole.pos = *pos;
    return object;

}

//4th Structure
phylib_object *phylib_new_hcushion(double y){ 

    phylib_object *object = malloc(sizeof(phylib_object)); 

    if (object == NULL){

        return NULL; 

    }

    object->type = PHYLIB_HCUSHION; 
    object->obj.hcushion.y = y; 
    return object; 

}

//5th Structure
phylib_object *phylib_new_vcushion( double x ){

    phylib_object *object = malloc(sizeof(phylib_object)); 

    if (object == NULL){

        return NULL; 

    }

    object->type = PHYLIB_VCUSHION; 
    object->obj.vcushion.x = x; 
    return object; 

}


phylib_table *phylib_new_table(void) {

    phylib_table *table = malloc(sizeof(phylib_table));

    //if (!table) return NULL;

    if (table == NULL){

        return NULL;

    }

    table->time = 0.0;
    
    // Initialize all object pointers to NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        table->object[i] = NULL;

    }

    // Adding horizontal cushions
    phylib_coord hcushion_pos1 = {0.0, 0.0};
    table->object[0] = phylib_new_hcushion(hcushion_pos1.y);

    phylib_coord hcushion_pos2 = {0.0, PHYLIB_TABLE_LENGTH};
    table->object[1] = phylib_new_hcushion(hcushion_pos2.y);

    // Adding vertical cushions
    phylib_coord vcushion_pos1 = {0.0, 0.0};
    table->object[2] = phylib_new_vcushion(vcushion_pos1.x);

    phylib_coord vcushion_pos2 = {PHYLIB_TABLE_WIDTH, 0.0};
    table->object[3] = phylib_new_vcushion(vcushion_pos2.x);

    // Adding holes
    // Corner holes and middle holes (total 6)
    phylib_coord hole_positions[6] = {
        {0.0, 0.0}, {0.0, PHYLIB_TABLE_LENGTH / 2.0},
        {0.0, PHYLIB_TABLE_LENGTH}, {PHYLIB_TABLE_WIDTH, 0.0},
        {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2.0}, {PHYLIB_TABLE_WIDTH , PHYLIB_TABLE_LENGTH}
    };

    for (int i = 0; i < 6; i++) {

        table->object[4 + i] = phylib_new_hole(&(hole_positions[i]));

    }

    // The remaining positions are initialized to NULL and can be filled with balls or other objects as needed
    return table;
}




// PART II

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    if (*src == NULL){

        *dest = NULL;

    }
    else{

        // Allocate memory for the new phylib_object
        *dest = (phylib_object *)malloc(sizeof(phylib_object));

        if(*dest != NULL) {

            memcpy(*dest, *src, sizeof(phylib_object));

        }

    }

    
}

phylib_table *phylib_copy_table( phylib_table *table ){

    if (table == NULL) {

        return NULL;

    }

    //Allocate memory 
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    new_table->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {

        
        phylib_copy_object( &(new_table->object[i]) , &(table->object[i])); 


    }
    return new_table;
    

}

void phylib_add_object( phylib_table *table, phylib_object *object ) {

    if (table == NULL || object == NULL){

        return;

    }

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        if(table->object[i] == NULL){

            table->object[i] = object;
            break;

        }


    }
}

void phylib_free_table( phylib_table *table ){

    if (table == NULL){

        return;

    }

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

        free(table->object[i]);
        table->object[i] = NULL;

    }
    free(table);



}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

    phylib_coord result;

    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
    
}

double phylib_length( phylib_coord c ){

    double length = sqrt((c.x * c.x) + (c.y * c.y));

    return length;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){

    double dotProduct = ((a.x * b.x) + (a.y * b.y));

    return dotProduct;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) { // changed this
        
        return -1.0;

    }

    phylib_coord diff;
    double distance;

    switch (obj2->type) {

        case PHYLIB_STILL_BALL:

            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
            distance = phylib_length(diff);
            return distance - PHYLIB_BALL_DIAMETER;
            break;


        case PHYLIB_ROLLING_BALL:

            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
            distance = phylib_length(diff);
            return distance - PHYLIB_BALL_DIAMETER;
            break;

        case PHYLIB_HOLE:

            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
            distance = phylib_length(diff);
            return distance - PHYLIB_HOLE_RADIUS;
            break;

        case PHYLIB_HCUSHION:{

            double pink = obj2->obj.hcushion.y;
            double blue = obj1->obj.rolling_ball.pos.y;
            
            distance = fabs(blue - pink);
            return distance - PHYLIB_BALL_RADIUS;
            break;}

        case PHYLIB_VCUSHION:{
        
            double pink = obj2->obj.vcushion.x;
            double blue = obj1->obj.rolling_ball.pos.x;
            
            distance = fabs(blue - pink);
            return distance - PHYLIB_BALL_RADIUS;
            break;}

        default:
            return -1.0; // obj2 is not a valid type
    }
}
    


// PART III

void phylib_roll( phylib_object *new, phylib_object *old, double time ) {

    //phylib_object *object = malloc(sizeof(phylib_object));

   
    if(new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL){

        return;

    }

    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * time * time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * time * time;

    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;


    if (new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if (new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }

}

unsigned char phylib_stopped( phylib_object *object ){


    if(object->type != PHYLIB_ROLLING_BALL || object == NULL){

        return 0;

    }

   if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON){

        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;

        return 1;

   }
   return 0;

 
}

void phylib_bounce( phylib_object **a, phylib_object **b ){

    if (*a == NULL || a == NULL || *b == NULL || b == NULL || (*a)->type != PHYLIB_ROLLING_BALL){

        return;

    }

    switch ((*b)->type){

        case PHYLIB_HCUSHION:

            (*a)->obj.rolling_ball.vel.y *= -1.0;
            (*a)->obj.rolling_ball.acc.y *= -1.0;
            break;

        case PHYLIB_VCUSHION:

            (*a)->obj.rolling_ball.vel.x *= -1.0;
            (*a)->obj.rolling_ball.acc.x *= -1.0;
            break;

        case PHYLIB_HOLE:

            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL:

            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

        
        case PHYLIB_ROLLING_BALL:{

            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            double r_ab_length = phylib_length(r_ab);
            // if (r_ab_length < PHYLIB_BALL_DIAMETER) {
                // Normalize r_ab
                phylib_coord n = { r_ab.x / r_ab_length, r_ab.y / r_ab_length };

                // Dot product of v_rel and n
                double v_rel_n = phylib_dot_product(v_rel, n);

                // Update velocities of both balls
                (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
                (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

                (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
                (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

                // Update accelerations based on new velocities
                double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
                double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

                if (speed_a > PHYLIB_VEL_EPSILON) {
                    (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG;
                    (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG;
                }

                if (speed_b > PHYLIB_VEL_EPSILON) {
                    (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG;
                }
                break;

            //}
        }

    }
}   




unsigned char phylib_rolling( phylib_table *t ){

    if (t == NULL){

        return 0;

    }

    unsigned char count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        
        if (t->object[i] && t->object[i]->type == PHYLIB_ROLLING_BALL){

            count++;

        }

    }
    return count;
}

//improved segemnt
phylib_table *phylib_segment(phylib_table *table){

    if((phylib_rolling(table) == 0)){

        return NULL;

    }

    //for time loop
    phylib_table *new_table = phylib_copy_table(table);
    double time;
    time = table->time + PHYLIB_SIM_RATE;

    while(time < PHYLIB_MAX_TIME){

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {

            if(new_table->object[i] && new_table->object[i]->type == PHYLIB_ROLLING_BALL){

                phylib_roll(new_table->object[i],new_table->object[i],PHYLIB_SIM_RATE);

                if(phylib_stopped(new_table->object[i])){

                    new_table->time = time;

                    return new_table;
                } 
            }
        }

        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){

            if(new_table->object[j] && new_table->object[j]->type == PHYLIB_ROLLING_BALL){

                for (int x = 0; x < PHYLIB_MAX_OBJECTS; x++){

                    if(new_table->object[x] != NULL && new_table->object[j] != new_table->object[x] && phylib_distance(new_table->object[j], new_table->object[x]) < 0.0){

                        phylib_bounce(&new_table->object[j],&new_table->object[x]);
                        new_table->time = time;
                        return new_table;

                    }
                }
            }
        }   
        //update the table time for every pass of the time loop
        time += PHYLIB_SIM_RATE;
    }
    new_table->time = time;
    return new_table;
}

char *phylib_object_string( phylib_object *object ){

    static char string[80]; if (object==NULL){

        snprintf( string, 80, "NULL;" ); return string;

    }

    switch (object->type){

        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number, object->obj.still_ball.pos.x, object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL: 
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", object->obj.rolling_ball.number, object->obj.rolling_ball.pos.x, object->obj.rolling_ball.pos.y, object->obj.rolling_ball.vel.x, object->obj.rolling_ball.vel.y, object->obj.rolling_ball.acc.x, object->obj.rolling_ball.acc.y );
            break;

        case PHYLIB_HOLE: 
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)", object->obj.hole.pos.x, object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION: 
            snprintf( string, 80,
            "HCUSHION (%6.1lf)", object->obj.hcushion.y );
            break;


        case PHYLIB_VCUSHION: 
            snprintf( string, 80,
            "VCUSHION (%6.1lf)", object->obj.vcushion.x );
            break; 
        
    }

  return string;
}
